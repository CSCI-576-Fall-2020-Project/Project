from flask import Flask, render_template, request

app = Flask(__name__)


# endpoint for index.html
@app.route('/', methods=["GET", "POST"])
def homePage():
    if request.method == "GET":
        return render_template("index.html")
    else:
        videoes = [[0, "flower.rgb", "90%"],
                   [1, "cars.rgb", "50%"],
                   [2, "movie.rgb", "10%"],
                   [3, "interview.rgb", "10%"]
                   ]
        query = request.form.get("query")
        return render_template("search_results.html",
                               given_query=query,
                               matched_videos=videoes)


if __name__ == '__main__':
    app.run()
