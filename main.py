from flask import Flask, render_template, request
import scrapeRedditURLs

app = Flask(__name__)
@app.route("/")
def search_home():
    return render_template("searchbar.html")

@app.route('/', methods=['POST'])
def search_home_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


@app.route("/links")
def search_links():
    # links = scrapeRedditURLs.redditURLs
    links = scrape(search_home_post())
    return render_template("links.html", links=links)

if __name__ == "__main__":
    app.run(debug=True)
