from flask import Flask, request, render_template, redirect, url_for
import json
import scraper
from user_system import *
from extra import *

app = Flask(__name__)

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
                attrs = manage_scraping(request.form,numofattrs)
        return render_template("main.html", attrs=attrs, num_of_attrs=int(numofattrs))

@app.route("/login",methods=["GET","POST"])
def log_in():
        return render_template("connect.html", operation="Log in", message="", url="/user")

@app.route("/register",methods=["GET","POST"])
def register():
        message = ""
        if request.method == "POST":
                if User.register(request.form["username"],request.form["password"]):
                        message = "registered successfully!"
                else:
                        message = "Username already taken!"
        return render_template("connect.html", operation="Register", message=message)

@app.route("/user",methods=["GET","POST"])
def welcome_user():
        if request.method == "POST":
                if User.get_user(request.form["username"],request.form["password"]):
                        return render_template("welcome.html",username=request.form["username"])
                else:
                        return render_template("failed.html")
        else:
                return "It seems like you're messing up with urls. Don't you?"

@app.route("/main_user",methods=["GET","POST"])
def main_user():
        return "Todo"

if __name__ == '__main__':
        app.run(host="0.0.0.0")
