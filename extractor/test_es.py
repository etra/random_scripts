import fire
from datetime import datetime
from elasticsearch import Elasticsearch
from pathlib import Path
import json
es = Elasticsearch(
    hosts=[{'scheme': 'http', 'host': 'localhost', 'port': 9200}],
)


# results = es.search(index="stuff", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % results['hits']['total']['value'])
# for hit in results['hits']['hits']:
#     print(hit)
#     exit()  

doc = es.get(index="stuff", id="128.101.101.254")
print(doc)