from app import app
from flask import render_template
from flask import request, redirect, url_for
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

        # иногда es отвечает не сразу, либо как то криво, из за чего возвращает
        # ошибку connection refused. помогло либо то, что я поставил retry, либо
        # то, что засунул все в один докер-композ и начал обращаться не по
        # localhost, а по elasticsearch
        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500,502,503,504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        params = {'size': 10000, }
        es_hits_resp = s.get('http://elasticsearch:9200/algorithms-events/_search',
                             params=params,
                             json=data_for_cache_hits,
                             verify=False)
        es_hits_data = es_hits_resp.json()


        hits_qty = es_hits_data['hits']['total']
        hits_data = [hit['_source'] for hit in es_hits_data['hits']['hits']]
        print(hits_qty)
        print(hits_data)

        # для того, чтобы выводить в сортированном виде в шаблонах, нужно
        # сделать целочисленный тип данных (да и вообще, по смыслу это поле
        # является целочисленным)
        for hit in hits_data:
            hit['popularity'] = int(hit['popularity'])
        return render_template('search_by_name.html',
                               search_object=search_object,
                               search_lang=search_lang,
                               hits_data=hits_data)

    return render_template('search_by_name.html')

@app.route('/update_es', methods=["GET"])
def update_es():
    topic = request.args.get("topic")
    language = request.args.get("language")
    params = {
        "project":  "algo_search",
        "spider":   "github",
        "topic":    topic,
        "language": language,
    }
    with requests.post("http://scrapyd:6800/schedule.json", params=params) as resp:
        print(resp.status_code)
        print(resp.json())

    return redirect(url_for("search_by_name",
                            search_object=topic,
                            search_lang=language))

@app.route('/clear_es', methods=["GET"])
def clear_es():
    topic = request.args.get("topic")
    language = request.args.get("language")

    data = {"query": {"match_all": {}}}
    with requests.post("http://elasticsearch:9200/algorithms-events/_delete_by_query",
                       json=data) as resp:
        print(resp.status_code)
        print(resp.json())

    return redirect(url_for("search_by_name",
                            search_object=topic,
                            search_lang=language))

@app.route('/search_by_type', methods=["GET", "POST"])
def search_by_type():
    search_object = request.args.get("search_object")
    return render_template('search_by_type.html',
                           search_object=search_object)
