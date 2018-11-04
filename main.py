from flask import Flask, render_template, request, url_for, flash, redirect
import Interfacer
import json

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
    objs = Interfacer.search(the_text)
    # lets = {}
    # for i in objs:
    #     lets.append(vars(objs))
    # links = []
    # for obj in objs:
    #     json_readable = json.dumps(obj, default=lambda o: o.__dict__)
    #     links.append(json_readable)
    # print(links)
    # for i in links:
    #     print(i["prod_name"])
    names = []
    scores = []
    links = []
    for i in objs:
        ob_dict = vars(i)
        names.append(ob_dict["prod_name"])
        scr = str(ob_dict["score"])
        scores.append(scr)
        links.append(ob_dict["link"])
    # real_names = []
    # for i in names:
    #     json_readable = json.dumps(obj, default=lambda o: o.__dict__)
    #     links.append(json_readable)
    return render_template("links.html", links=links, names=names, scores=scores)

if __name__ == "__main__":
    app.run(debug=True)
