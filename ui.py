from flask import Flask,request,render_template
import scraper

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
        data = []
        numOfSites = 0
        if request.method == "POST":
                if request.form["attrVal"]:

                        if request.form["attrToScrape"]:
                                data = scraper.scrape_objects_attr_by_attr(request.form["oaType"],request.form["attrVal"],request.form["link"],request.form["attrToScrape"])
                        else:
                                data = scraper.scrape_objects_text_by_attr(request.form["oaType"],request.form["attrVal"],request.form["link"])
                else:
                        if request.form["attrToScrape"]:
                                data = scraper.scrape_objects_attr_by_type(request.form["oaType"],request.form["link"],request.form["attrToScrape"])
                        elif request.form["link"]:
                                data = scraper.scrape_objects_text_by_type(request.form["oaType"],request.form["link"]) 

        return render_template("base.html",data=data)

if __name__ == '__main__':
        app.run()
