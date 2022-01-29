from flask import Flask,request,render_template, redirect
import scraper
from user_system import *

app = Flask(__name__)

@app.route("/")
def homepage():
        return redirect("/main/0")

@app.route("/main/<numofattrs>",methods=["GET","POST"])
def main(numofattrs):
        rules = {}
        attrs = {}
        attrnames = []
        results = []
        if request.method == "POST":
                if request.form["numofattrstoscrape"]:
                        return redirect(f"/main/{request.form['numofattrstoscrape']}")
                if request.form["objectType"]:
                        rules["objectType"] = request.form["objectType"]
                if request.form["attr"] and request.form["attrVal"]:
                        rules["attr"] = [request.form["attr"],request.form["attrVal"]]
                for i in range(int(numofattrs)):
                        attrnames.append(request.form[f"attrToScrape{i}"])
                for i,rule in enumerate(rules):
                        results.append([])
                        if rule == "objectType":
                                for attrname in attrnames:
                                         for instance in scraper.scrape_object_by_type(rules[rule],request.form["link"],attrname):
                                                 results[i].append({attrname:instance})
                        elif rule == "attr":
                                for attrname in attrnames:
                                        for instance in scraper.scrape_object_by_attr(rules[rule][0],rules[rule][1],request.form["link"],attrname):
                                                 results[i].append({attrname:instance})
                attrs = formatlst(onlydups(results))
        return render_template("main.html", attrs=attrs, numofattrs=int(numofattrs))

@app.route("/login",methods=["GET","POST"])
def login():
        message = ""
        if request.method == "POST":
                if User.get_user(request.form["username"],request.form["password"]):
                        message = "logged in successfully!"
                else:
                        message = "failed to log in!"
        return render_template("user.html", operation="log in", message=message)

@app.route("/register",methods=["GET","POST"])
def register():
        message = ""
        if request.method == "POST":
                User.register(request.form["username"],request.form["password"])
                message = "registered successfully!"
        return render_template("user.html", operation="register", message=message)

def onlydups(lstoflsts):
        toRet = []
        samplelst = lstoflsts.pop()
        for lst in lstoflsts:
                for i,item in enumerate(samplelst):
                        if not item in samplelst:
                                samplelst[i] = False
        for item in samplelst:
                if item != False:
                        toRet.append(item)
        return toRet

def formatlst(lst):
        toRet = {}
        for i,pair in enumerate(lst):
                for key in pair:
                        if key in toRet:
                                toRet[key].append(pair[key])
                        else:
                                toRet[key] = [pair[key]]
        return toRet
                                        
if __name__ == '__main__':
        app.run(host="0.0.0.0")
