from flask import Flask,request,render_template, redirect
import scraper
from user_system import *
from extra import *

app = Flask(__name__)

@app.route("/")
def home_page():
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
def log_in():
        message = ""
        if request.method == "POST":
                if User.get_user(request.form["username"],request.form["password"]):
                        return redirect(f"/user/{request.form['username']}")
                else:
                        message = "failed to log in!"
        return render_template("connect.html", operation="log in", message=message)

@app.route("/register",methods=["GET","POST"])
def register():
        message = ""
        if request.method == "POST":
                User.register(request.form["username"],request.form["password"])
                message = "registered successfully!"
        return render_template("connect.html", operation="register", message=message)

@app.route("/user/<user>",methods=["GET","POST"])
def main_user(user):
        return "Hello " + user

if __name__ == '__main__':
        app.run(host="0.0.0.0")
