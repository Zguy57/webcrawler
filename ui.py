from flask import Flask, request, render_template, redirect, url_for, make_response
import json
import scraper
from user_system import *
from extra import *

app = Flask(__name__)
app.secret_key = "abcdefg"

@app.route("/")
def home_page():
        return redirect("/main/0")

def manage_scraping(form,numofattrs):
        rules = {}
        attrs = {}
        attrnames = []
        results = []  
        if form["objectType"]:
                        rules["objectType"] = form["objectType"]
        if form["attr"] and form["attrVal"]:
                rules["attr"] = [form["attr"],form["attrVal"]]
        for i in range(int(numofattrs)):
                attrnames.append(form[f"attrToScrape{i}"])
        for i,rule in enumerate(rules):
                results.append([])
                if rule == "objectType":
                        for attrname in attrnames:
                                  for instance in scraper.scrape_object_by_type(rules[rule],form["link"],attrname):
                                          results[i].append({attrname:instance})
                elif rule == "attr":
                        for attrname in attrnames:
                                for instance in scraper.scrape_object_by_attr(rules[rule][0],rules[rule][1],form["link"],attrname):
                                          results[i].append({attrname:instance})
        attrs = format_lst(only_dups(results))
        return attrs

@app.route("/main/<numofattrs>",methods=["GET","POST"])
def main(numofattrs):
        attrs={}
        if request.method == "POST":
                if request.form["numofattrstoscrape"]:
                        return redirect(f"/main/{request.form['numofattrstoscrape']}")
                attrs = manage_scraping(request.form, numofattrs)
        return render_template("main.html", attrs=attrs, num_of_attrs=int(numofattrs), redirect_url=f"/main/{int(numofattrs)}", username="Guest")

@app.route("/login",methods=["GET","POST"])
def log_in():
        return render_template("connect.html", operation="Log in", message="", url="/welcome_user")

@app.route("/register",methods=["GET","POST"])
def register():
        message = ""
        if request.method == "POST":
                if User.register(request.form["username"], request.form["password"]):
                        message = "registered successfully!"
                else:
                        message = "Username already taken!"
        return render_template("connect.html", operation="Register", message=message)

@app.route("/welcome_user",methods=["GET","POST"])
def welcome_user():
        if request.method == "POST":
                user = User.get_user(request.form["username"], request.form["password"])
                if user:
                        resp = make_response(render_template("welcome.html", username=request.form["username"], history=user.get_history()))
                        resp.set_cookie("username", request.form["username"])
                        return resp
                else:
                        return render_template("failed.html")
        else:
                return "It seems like you're messing up with urls. Don't you?"

@app.route("/main_user", methods=["GET","POST"])
def main_user():
        if request.method == "POST":
                if "objectType" not in request.form or "num_of_attrs" in request.form:
                        resp = make_response(render_template("main.html", attrs={}, num_of_attrs=int(request.form["num_of_attrs"]), redirect_url="/main_user"))
                        resp.set_cookie("num_of_attrs", request.form["num_of_attrs"])
                        return resp
                attrs = manage_scraping(request.form, int(request.cookies.get("num_of_attrs")))
                Online[request.cookies.get("username")].log_scrape(attrs)
                return render_template("main.html", attrs=attrs, num_of_attrs=int(request.cookies.get("num_of_attrs")), redirect_url="main_user")
        else:
                return "It seems like you're messing up with urls. Don't you?" 

@app.route("/view_history", methods=["GET","POST"])
def view_history():
        userslst = []
        for user in db:
                userslst.append(json.loads(db[user]))
        return render_template("view_history.html", users=userslst)

if __name__ == '__main__':
        app.run(host="0.0.0.0")
