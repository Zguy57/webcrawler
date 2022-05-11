from flask import Flask, request, render_template, redirect, url_for, make_response
import json
import scraper
from user_system import *
from extra import *
import ssl
import smtplib

app = Flask(__name__)

SENDER = ""
PASSWORD = ""


@app.route("/")
def home_page():
    '''This function redirects the user to the site.'''
    return redirect("/main")


def manage_scraping(form, final_stage):
    '''This function uses the different scraping functions in order to satisfy the user needs.'''
    rules = {}
    attrs = []
    attrnames = form["attrsToScrape"].split("|")
    results = []
    #Inserting the rules that the user set
    if form["objectType"]:
        rules["objectType"] = form["objectType"]
    if form["attr"] and form["attrVal"]:
        rules["attr"] = [form["attr"], form["attrVal"]]
    #The case when the user decides to scrape the data in one stage
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
    #The case of the first stage
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
    #The case of the last stage
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
    #The case of the second, third and so on but not the last stage
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
    '''This function is responsible for rendering the main page.'''
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
                           final_stage=final_stage,
                           back_url="/login",
                           back_text="Log in")


@app.route("/login", methods=["GET", "POST"])
def log_in():
    '''This function is responsible for rendering the login page.'''
    return render_template("connect.html",
                           operation="Log in",
                           message="",
                           url="/user_page",
                           show_username=True,
                           show_password=True,
                           show_confirm=False,
                           show_email=False,
                           back_url="/register",
                           back_text="Register")


@app.route("/register", methods=["GET", "POST"])
def register():
    '''This function is responsible for rendering the register page.'''
    message = ""
    if request.method == "POST":
        if request.form["password"] == request.form[
                "confirmPassword"] and User.register(request.form["username"],
                                                     request.form["password"],
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
                           show_confirm=True,
                           show_email=True,
                           back_url="/login",
                           back_text="Log in")


@app.route("/user_page", methods=["GET", "POST"])
def user_page():
    '''This function is responsible for rendering the user page'''
    if request.method == "POST":
        if "submit" in request.form and request.form["submit"] == "Delete":
            Online[request.cookies.get("username")].delete_scrape(request.form["scrapeId"])
            return render_template(
            "user_page.html",
            username=request.cookies.get("username"),
            history=Online[request.cookies.get("username")].get_history(),
            is_manager=request.cookies.get("username") in db["managers"])
        else:
            user = User.get_user(request.form["username"],
                                 request.form["password"])
            if user:
                resp = make_response(
                    render_template("user_page.html",
                                    username=request.form["username"],
                                    history=user.get_history(),
                                    is_manager=request.form["username"]
                                    in db["managers"]))
                resp.set_cookie("username", request.form["username"])
                return resp
            else:
                return render_template("failed.html")
    elif request.cookies.get("username") in Online:
        return render_template(
            "user_page.html",
            username=request.cookies.get("username"),
            history=Online[request.cookies.get("username")].get_history(),
            is_manager=request.cookies.get("username") in db["managers"])

    else:
        return "It seems like you're messing up with urls. Don't you?"


@app.route("/nav_user", methods=["GET", "POST"])
def nav_user():
    '''This function navigates the user to the requested page he chose in the user page.'''
    if request.method == "POST":
        if request.form["submit"] == "Begin scraping":
            return redirect("/main_user")
        elif request.form["submit"] == "Change password":
            return redirect("/change_password")
        elif request.form["submit"] == "Manager page":
            return redirect("/manager_page")
        elif request.form["submit"] == "Log out":
            Online[request.cookies.get("username")].log_out()
            return redirect("/main")
    else:
        return "It seems like you're messing up with urls. Don't you?"


@app.route("/main_user", methods=["GET", "POST"])
def main_user():
    '''This function is responsible for rendering the main page which is also linked to the user and its history.'''
    if request.cookies.get("username"):
        final_stage = False
        attrs = {}
        if "attrsToScrape" in request.form and request.form["attrsToScrape"]:
            final_stage = True
        if "attrsToScrape" in request.form:
            attrs = manage_scraping(request.form, final_stage)
        if final_stage:
            Online[request.cookies.get("username")].log_scrape(attrs)
        return render_template("main.html",
                               attrs=attrs,
                               redirect_url="main_user",
                               final_stage=final_stage,
                               back_url="/user_page",
                               back_text="Go back")
    else:
        return "You're logged out!"


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    '''This function is responsible for rendering the change password page.'''
    message = ""
    username = request.cookies.get("username")
    if username:
        if request.method == "POST":
            if request.form["password"] == request.form["confirmPassword"]:
                Online[username].change_password(request.form["password"])
                message = "Password changed successfully!"
            else:
                message = "Passwords don't match!"
        return render_template("connect.html",
                               operation="Change password",
                               message=message,
                               url="/change_password",
                               show_username=False,
                               show_password=True,
                               show_confirm=True,
                               show_email=False,
                               back_url="/user_page",
                               back_text="Go back")
    else:
        return "Error!"


@app.route("/manager_page", methods=["GET", "POST"])
def manager_page():
    '''This function is responsible for rendering the manager page.'''
    message = ""
    if request.method == "POST":
        if request.form["submit"] == "Submit":
            if request.form["operation"] == "ban user":
                if request.form["username"] in db["users"]:
                    Online[request.cookies.get("username")].ban_user(
                        request.form["username"])
                    message = "Operation executed successfully!"
                else:
                    message = "Invalid username!"
            elif request.form["operation"] == "unban user":
                if request.form["username"] in db["banned"]:
                    Online[request.cookies.get("username")].unban_user(
                        request.form["username"])
                    message = "Operation executed successfully!"
                else:
                    message = "Invalid username!"
            else:
                message = "Invalid operation!"
        elif request.form["submit"] == "Show managers history":
            return redirect("/manager_history")
        elif request.form["submit"] == "Show users history":
            return redirect("/user_history")
        elif request.form["submit"] == "Go back":
            return redirect("/user_page")
    if request.cookies.get("username") in db[
            "managers"] and request.cookies.get("username") in Online:
        return render_template("manager_page.html", message=message)
    else:
        return "Error!"


@app.route("/manager_history", methods=["GET", "POST"])
def manager_history():
    '''This function is responsible for rendering the manager history page.'''
    if request.cookies.get("username") in db["managers"]:
        history = []
        if "userRegex" in request.form:
            try:
                for manager in db["managers"]:
                    if not (request.form["userRegex"]) or re.fullmatch(
                            str(request.form["userRegex"]), manager):
                        toAppend = {"username": manager}
                        toAppend["operations"] = []
                        for operation_id in db["managers"][manager][
                                "_management_history"]:
                            operation = db["operations"][str(operation_id)]
                            toAppend["operations"].append(
                                str(
                                    ManagerOperation(
                                        operation["_operation"],
                                        operation["_username"],
                                        operation["_time"],
                                        operation["_operation_id"])))
                        history.append(toAppend)
            except:
                return "Invalid regular expression!"
        else:
            for manager in db["managers"]:
                toAppend = {"username": manager}
                toAppend["operations"] = []
                for operation_id in db["managers"][manager][
                        "_management_history"]:
                    operation = db["operations"][str(operation_id)]
                    toAppend["operations"].append(
                        str(
                            ManagerOperation(operation["_operation"],
                                             operation["_username"],
                                             operation["_time"],
                                             operation["_operation_id"])))
                history.append(toAppend)
        return render_template("show_history.html",
                               which="manager",
                               history=history)
    else:
        return "Error!"


@app.route("/user_history", methods=["GET", "POST"])
def user_history():
    '''This function is responsible for rendering the users' history page.'''
    if request.cookies.get("username") in db["managers"]:
        users = []
        if "userRegex" in request.form:
            try:
                for user in db["users"]:
                    if (not request.form["userRegex"]) or re.fullmatch(
                            str(request.form["userRegex"]), user):
                        userObj = User(db["users"][user]["_username"],
                                       db["users"][user]["_password"],
                                       db["users"][user]["_email"],
                                       db["users"][user]["_history"])
                        users.append({
                            "username": user,
                            "history": userObj.get_history()
                        })
                for user in db["managers"]:
                    if (not request.form["userRegex"]) or re.fullmatch(
                            str(request.form["userRegex"]), user):
                        userObj = User(db["managers"][user]["_username"],
                                       db["managers"][user]["_password"],
                                       db["managers"][user]["_email"],
                                       db["managers"][user]["_history"])
                        users.append({
                            "username": user,
                            "history": userObj.get_history()
                        })
                for user in db["banned"]:
                    if (not request.form["userRegex"]) or re.fullmatch(
                            str(request.form["userRegex"]), user):
                        userObj = User(db["banned"][user]["_username"],
                                       db["banned"][user]["_password"],
                                       db["banned"][user]["_email"],
                                       db["banned"][user]["_history"])
                        users.append({
                            "username": user,
                            "history": userObj.get_history()
                        })
            except:
                return "Invalid regular expression!"
        else:
            for user in db["users"]:
                userObj = User(db["users"][user]["_username"],
                               db["users"][user]["_password"],
                               db["users"][user]["_email"],
                               db["users"][user]["_history"])
                users.append({
                    "username": user,
                    "history": userObj.get_history()
                })
            for user in db["managers"]:
                userObj = User(db["managers"][user]["_username"],
                               db["managers"][user]["_password"],
                               db["managers"][user]["_email"],
                               db["managers"][user]["_history"])
                users.append({
                    "username": user,
                    "history": userObj.get_history()
                })
            for user in db["banned"]:
                userObj = User(db["banned"][user]["_username"],
                               db["banned"][user]["_password"],
                               db["banned"][user]["_email"],
                               db["banned"][user]["_history"])
                users.append({
                    "username": user,
                    "history": userObj.get_history()
                })
        return render_template("show_history.html", which="user", users=users)
    else:
        return "Error!"


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    '''This function is responsible for rendering the forgot password/username page'''
    email_msg = ""
    message = ""
    if request.method == "POST":
        for user in db["users"]:
            if request.form["email"] == db["users"][user]["_email"]:
                email_msg += f"Username: {user}\n"
                password = random.randint(1000, 9999)
                email_msg += f"Password: {password}\n\n"
                db["users"][user]["_password"] = encrypt(user, str(password))
        if email_msg:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                                  context=context) as server:
                server.login(SENDER, PASSWORD)
                server.sendmail(
                    SENDER, request.form["email"],
                    f"Subject: Forgot password\n\nThese are the registered users we have:\n\n{email_msg}\nPlease change the new passwords as quickly as possible."
                )
            message = "Sent email!"
        else:
            message = "No registered users!"
    return render_template("connect.html",
                           operation="Send email",
                           show_username=False,
                           show_password=False,
                           show_confirm=False,
                           show_email=True,
                           message=message,
                           back_url="/login",
                           back_text="Log in")


if __name__ == '__main__':
    with open("mail.json", "r") as f:
        data = json.load(f)
        SENDER = data["email"]
        PASSWORD = data["password"]
    app.run(host="0.0.0.0")
