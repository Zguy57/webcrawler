from flask import Flask, request, render_template, redirect, url_for, make_response
import json
import scraper
from user_system import *
from extra import *

app = Flask(__name__)


@app.route("/")
def home_page():
    return redirect("/main")


def manage_scraping(form, final_stage):
    rules = {}
    attrs = []
    attrnames = form["attrsToScrape"].split("|")
    results = []
    if form["objectType"]:
        rules["objectType"] = form["objectType"]
    if form["attr"] and form["attrVal"]:
        rules["attr"] = [form["attr"], form["attrVal"]]
    if form["link"] and final_stage:
        for i, rule in enumerate(rules):
            results.append([])
            if rule == "objectType":
                for attrname in attrnames:
                    for instance in scraper.scr_obj_by_type(rules[rule],
                                                            attrname,
                                                            link=form["link"]):
                        results[i].append({attrname: instance})
            elif rule == "attr":
                for attrname in attrnames:
                    for instance in scraper.scr_obj_by_attr(rules[rule][0],
                                                            rules[rule][1],
                                                            attrname,
                                                            link=form["link"]):
                        results[i].append({attrname: instance})
        attrs = format_lst(only_dups(results))
    elif form["link"]:
        for i, rule in enumerate(rules):
            results.append([])
            if rule == "objectType":
                for instance in scraper.find_obj_by_type(rules[rule],
                                                         link=form["link"]):
                    results[i].append(instance)
            elif rule == "attr":
                for instance in scraper.find_obj_by_attr(rules[rule][0],
                                                         rules[rule][1],
                                                         link=form["link"]):
                    results[i].append(instance)
        attrs = only_dups(results)
    elif form["submit"] != "Submit" and final_stage:
        for i, rule in enumerate(rules):
            results.append([])
            if rule == "objectType":
                for attrname in attrnames:
                    for instance in scraper.scr_obj_by_type(
                            rules[rule], attrname, tree=form["submit"]):
                        results[i].append({attrname: instance})
            elif rule == "attr":
                for attrname in attrnames:
                    for instance in scraper.scr_obj_by_attr(
                            rules[rule][0],
                            rules[rule][1],
                            attrname,
                            tree=form["submit"]):
                        results[i].append({attrname: instance})
        attrs = format_lst(only_dups(results))
    elif form["submit"] != "Submit":
        for i, rule in enumerate(rules):
            results.append([])
            if rule == "objectType":
                for instance in scraper.find_obj_by_type(rules[rule],
                                                         tree=form["submit"]):
                    results[i].append(instance)
            elif rule == "attr":
                for instance in scraper.find_obj_by_attr(rules[rule][0],
                                                         rules[rule][1],
                                                         tree=form["submit"]):
                    results[i].append(instance)
        attrs = only_dups(results)
    return attrs


@app.route("/main", methods=["GET", "POST"])
def main():
    attrs = {}
    final_stage = False
    if request.method == "POST":
        if request.form["attrsToScrape"]:
            final_stage = True
        attrs = manage_scraping(request.form, final_stage)
    return render_template("main.html",
                           attrs=attrs,
                           redirect_url=f"/main",
                           username="Guest",
                           final_stage=final_stage)


@app.route("/login", methods=["GET", "POST"])
def log_in():
    return render_template("connect.html",
                           operation="Log in",
                           message="",
                           url="/welcome_user",
                           show_username=True,
                           show_password=True,
                           show_email=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        if User.register(request.form["username"], request.form["password"],
                         request.form["email"]):
            message = "Registered successfully!"
        else:
            message = "Failed to register!"
    return render_template("connect.html",
                           operation="Register",
                           message=message,
                           url="/register",
                           show_username=True,
                           show_password=True,
                           show_email=True)


@app.route("/welcome_user", methods=["GET", "POST"])
def welcome_user():
    if request.method == "POST":
        user = User.get_user(request.form["username"],
                             request.form["password"])
        if user:
            resp = make_response(
                render_template("welcome.html",
                                username=request.form["username"],
                                history=user.get_history()))
            resp.set_cookie("username", request.form["username"])
            return resp
        else:
            return render_template("failed.html")
    else:
        return "It seems like you're messing up with urls. Don't you?"


@app.route("/main_user", methods=["GET", "POST"])
def main_user():
    if request.method == "POST":
        final_stage = False
        if request.form["attrsToScrape"]:
            final_stage = True
        attrs = manage_scraping(request.form,
                                final_stage)
        if final_stage:
                Online[request.cookies.get("username")].log_scrape(attrs)
        return render_template("main.html",
                               attrs=attrs,
                               redirect_url="main_user", final_stage=final_stage)
    else:
        return "It seems like you're messing up with urls. Don't you?"


@app.route("/view_history", methods=["GET", "POST"])
def view_history():
    if request.cookies.get("username")[0] == "@":
        historylst = []
        for user in db:
            historylst.append((user, dict(json.loads(db[user]))["_history"]))
        return render_template("view_history.html", users=historylst)
    else:
        return "Not enough permissions!"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
