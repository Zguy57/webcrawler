from flask import Flask,request,render_template
import scraper

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
        data = []
        if request.method == "POST":
                data = scraper.scrape_objects(request.form["objType"],request.form["link"])
        return render_template("base.html",data=data)

if __name__ == '__main__':
        app.run()
