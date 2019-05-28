import re
import requests
import pickle
import os

# change url for your channel
API_URL = "Your Slack API"

# enter query relating your research
main = ''
sub1 = ''
sub2 = ''

def parse(data, tag):
    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ
    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj

def search_and_send(query, start, ids, slack_api_url):
    while True:
        counter = 0
        # detail is shown here, https://arxiv.org/help/api/user-manual
        # start is first searched index num
        # sortBy: submittedDate, lastUpdatedDate, relevance
        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(start) + '&max_results=100&sortBy=submittedDate&sortOrder=descending'
        # Get returned value from arXiv API
        print(url)
        data = requests.get(url).text
        # Parse the returned value
        entries = parse(data, "entry")
        for entry in entries:
            # Parse each entry
            url = parse(entry, "id")[0]
            if not(url in ids):
                title = parse(entry, "title")[0]
                #abstract = parse(entry, "summary")[0]
                date = parse(entry, "published")[0]
                if date.startswith("2016"):
                    return 0
                message = "\n".join(["=" * 10, "No." + str(counter + 1), "Title:  " + title, "URL: " + url, "Published: " + date])
                requests.post(slack_api_url, json={"text": message})
                ids.append(url)
                counter = counter + 1
                '''
                if counter == 10:
                    return 0
                '''

if __name__ == "__main__":
    print("Publish")
    slack_api_url = API_URL
    # Load log of published data
    if os.path.exists("published.pkl"):
        ids = pickle.load(open("published.pkl",'rb'))
    else:
        ids = []
    #   User Manual : 5.3. Subject Classifications
    query = "(cat:cs.CL)+AND+(ti:"+main+"\ )+AND+((abs:"+sub1+"\ )+OR+(abs:"+sub2+"\ ))"
    start = 0
    # Post greeting to your Slack
    requests.post(slack_api_url, json={"text": "2017年からのの投稿"})
    # Call function
    search_and_send(query, start, ids, slack_api_url)
    # Update log of published data
    pickle.dump(ids, open("published.pkl", "wb"))
