from flask import Flask, render_template, request
from difflib import SequenceMatcher
import main

app = Flask(__name__)

past_search = []
given_queries = ["ads_1.jpeg", "ads_2.jpeg", "cartoon_1.jpeg", "cartoon_2.jpeg", "concert_1.jpeg",
                 "interview_1.jpeg", "interview_2.jpeg", "movies_1.jpeg", "movies_2.jpeg",
                 "sport_1.jpeg"]

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
        if len(past_search) != 0:
            if len(past_search) == 3 and query not in past_search:
                del past_search[-1]
                past_search.insert(0, query)
            elif len(past_search) != 1 and query in past_search:
                index = past_search.index(query)
                del past_search[index]
                past_search.insert(0, query)
            elif query not in past_search:
                past_search.insert(0, query)
        else:
            past_search.insert(0, query)
        return render_template("search_results.html",
                               given_query=query,
                               matched_videos=videoes)

def getAutoCorrection(input):
    if input[-1] == ' ':
        return []  # return empty suggestions when user starts entering a new word
    else:
        inputs = input.split()
        if len(inputs) == 1:  # return correction on this word, removing all white spaces.
            re = []
            for query in given_queries:
                ratio = SequenceMatcher(None, query, inputs[0]).ratio()
                if query[0:len(inputs[0])] == inputs[0]:
                    ratio += 0.5
                if len(inputs[0]) >= 3 and ratio <= 0.3:
                    continue
                else:
                    re.append((query, ratio))
            re = sorted(re, key=lambda a: a[1], reverse=True)
            results = []
            for r in re:
                if(len(results) == 5):
                    break
                else:
                    results.append(r[0])
            return results

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args["query"]
    return {"history": past_search,
            "autocorrect": getAutoCorrection(query)}

if __name__ == '__main__':

    app.run()
