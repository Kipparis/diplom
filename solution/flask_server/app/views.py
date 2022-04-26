from app import app
from flask import render_template
from flask import request, redirect
import requests
from requests.adapters import HTTPAdapter, Retry

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/repository/<hostname>/<reponame>')
def show_repository(hostname, reponame):
    return f"Showing repository located on {hostname} with name {reponame}"

@app.route('/search_by_name', methods=["GET", "POST"])
def search_by_name():
    search_object = request.args.get("search_object")
    search_lang = request.args.get("search_lang")
    print(search_object)
    print(search_lang)
    if search_object is not None and search_lang is not None:
        # return cached results and display button "requery"
        data_for_cache_hits = { # elastic search data query
            "query": {
                "bool": {
                    "must": [
                        {"match": {"topic": search_object}},
                        {"match": {"language": search_lang}},
                    ]
                }
            },
        }
        print(data_for_cache_hits)

        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500,502,503,504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        es_hits_resp = s.get('http://elasticsearch:9200/algorithms-events/_search?pretty',
                                    json=data_for_cache_hits,
                                    verify=False)
        es_hits_data = es_hits_resp.json()


        hits_qty = es_hits_data['hits']['total']
        hits_data = [hit['_source'] for hit in es_hits_data['hits']['hits']]
        print(hits_qty)
        print(hits_data)

    return render_template('search_by_name.html',
                           search_object=search_object,
                           search_lang=search_lang)

@app.route('/search_by_type', methods=["GET", "POST"])
def search_by_type():
    search_object = request.args.get("search_object")
    return render_template('search_by_type.html',
                           search_object=search_object)
