from flask import Flask,request,render_template
import scraper

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
        data = []
        if request.method == "POST":
                if not request.form["attr"]:
                        data = scraper.scrape_objects_text(request.form["objType"],request.form["link"])
                else:
                        data = scraper.scrape_objects_attr(request.form["objType"],request.form["link"],request.form["attr"])
        return render_template("base.html",data=data)

if __name__ == '__main__':
        app.run()
