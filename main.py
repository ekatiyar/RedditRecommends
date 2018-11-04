from flask import Flask, render_template, request, url_for, flash, redirect
import scrapeRedditURLs

app = Flask(__name__)
@app.route("/")
def search_home():
    return render_template("searchbar.html")

# @app.route('/process', methods=['POST'])
# def process():
#     the_text = request.form['some_data']
#     return "text is:" + the_text


@app.route("/search_links", methods=['POST'])
def search_links():
    the_text = request.form['some_data']
    links = scrapeRedditURLs.scrape(the_text)
    return render_template("links.html", links=links)

if __name__ == "__main__":
    app.run(debug=True)
