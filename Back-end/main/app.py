from flask import Flask, render_template, request, session
from difflib import SequenceMatcher
from videoQuery import videoQuery
import pickle

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

past_search = []
saved_results = []

# given_queries = ["ads_1.jpeg", "ads_2.jpeg", "cartoon_1.jpeg", "cartoon_2.jpeg", "concert_1.jpeg",
#                  "interview_1.jpeg", "interview_2.jpeg", "movies_1.jpeg", "movies_2.jpeg",
#                  "sport_1.jpeg"]
given_queries = ["ads_1", "ads_2", "cartoon_1", "cartoon_2", "concert_1",
                 "interview_1", "interview_2", "movies_1", "movies_2",
                 "sport_1"]


# endpoint for index.html
@app.route('/', methods=["GET", "POST"])
def homePage():
    if request.method == "GET":
        session['saved_query'] = ""
        session['saved_matched_videos'] = []
        return render_template("index.html", noResults=False)
    else:
        # print(getQueryVideoLink(request.form.get("query")))
        # return render_template("search_results.html",
        #                        given_query=session.get('saved_query'),
        #                        matched_videos=session.get('saved_matched_videos'),
        #                        video_link=getVideoLink("ads_1"),
        #                        original_video_link=getQueryVideoLink(request.form.get("query")),
        #                        query_data_size=0,
        #                        query_data=[],
        #                        database_data_Size=0,
        #                        database_data=[],
        #                        current_query=1)
        session['saved_query'] = ""
        saved_results.clear()
        session['saved_matched_videos'] = []
        if request.form.get("query") not in given_queries:
            return render_template("index.html", noResults=True)
        query = request.form.get("query")
        input_query = query.split('.')[0]
        input_query = "test_jpg/" + input_query
        print(input_query)
        results = videoQuery([input_query])
        # output = open("output.pkl", 'wb')
        # pickle.dump(results, output)
        # output.close()
        # pkl_file2 = open("output.pkl", 'rb')
        # results = pickle.load(pkl_file2)
        # savePastSearches(query)
        # result_size = len(results)
        print(results)
        matched_videos = []
        for search_result in results:
            # matched_videos.append(((search_result.videoName + ".jpeg"), int(100/float(search_result.totalScore))))
            matched_videos.append(((search_result.videoName), int(100 / float(search_result.totalScore))))
            saved_results.append(search_result)
        matched_videos = sorted(matched_videos, key= lambda a: a[1], reverse=True)
        data = getDataWithVideoName(matched_videos[0][0])
        session['saved_query'] = query
        session['saved_matched_videos'] = matched_videos
        return render_template("search_results.html",
                               given_query=session.get('saved_query'),
                               matched_videos=session.get('saved_matched_videos'),
                               video_link=getVideoLink(session.get('saved_matched_videos')[0][0]),
                               original_video_link=getQueryVideoLink(query),
                               query_data_size=data[0]-1,
                               query_data=data[1],
                               database_data_Size=data[2]-1,
                               database_data=data[3],
                               current_query=matched_videos[0][0])


def getVideoLink(matched_name):
    category = matched_name.split("_")[0]
    # name = matched_name.split(".")[0]
    # return "Videos/" + category + "/" + name + ".mp4"
    return "Videos/" + category + "/" + matched_name + ".mp4"

def getQueryVideoLink(query):
    # name = query.split(".")[0]
    # return "QueryVideos/" + name + ".mp4"
    return "QueryVideos/" + query + ".mp4"

def getDataWithVideoName(videoName):
    name = videoName.split(".")[0]
    query_keyFrames = []
    database_keyFrames = []
    database_size = 0
    query_data_size = 0
    for matched_result in saved_results:
        if matched_result.videoName == name:
            query_data_size = len(matched_result.queryKeyFrames)
            database_size = len(matched_result.dataKeyFrames)
            for frame in matched_result.dataKeyFrames.keys():
                database_keyFrames.append([int(frame[5:]), float(matched_result.dataKeyFrames[frame])])
            for frame in matched_result.queryKeyFrames.keys():
                query_keyFrames.append([int(frame[5:]), float(matched_result.queryKeyFrames[frame])])
    database_keyFrames = sorted(database_keyFrames, key=lambda a:a[0])
    query_keyFrames = sorted(query_keyFrames, key=lambda a: a[0])
    return query_data_size, query_keyFrames, database_size, database_keyFrames


@app.route('/search_results/<string:jpeg_name>', methods=['GET', 'POST'])
def fetchSearchResultsOn(jpeg_name):
    print(jpeg_name)
    # data = getDataWithVideoName(jpeg_name + '.jpeg')
    data = getDataWithVideoName(jpeg_name)
    return render_template("search_results.html",
                           given_query=session['saved_query'],
                           matched_videos=session['saved_matched_videos'],
                           video_link=getVideoLink(jpeg_name),
                           original_video_link=getQueryVideoLink(session['saved_query']),
                           query_data_size=data[0]-1,
                           query_data=data[1],
                           database_data_Size=data[2]-1,
                           database_data=data[3],
                           current_query=jpeg_name)

def savePastSearches(query):
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