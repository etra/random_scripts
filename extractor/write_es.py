import fire
from datetime import datetime
from elasticsearch import Elasticsearch
from pathlib import Path
import json
es = Elasticsearch(
    hosts=[{'scheme': 'http', 'host': 'localhost', 'port': 9200}],
)

class Worker(object):
    """
        A worker scans provided source directory.
        Each file contains a json ND structure where single line in a file is a single document in ES.
        Worker index single file using bulk command to increase performance
    """

    source_dir: Path = None


    def _get_files(self):
        return self.source_dir.glob('*.json')

    def _index_file(self, file_path):
        bulk = []
        with open(file_path) as f:
            data = f.readlines()
            for line in data:
                js_doc = json.loads(line)
                bulk.append({'index': {'_index': 'stuff', '_id': js_doc['ip']}})
                bulk.append(js_doc)
        res = es.bulk(index='stuff', body=bulk)            
        print(res)

    def run(self, source_dir):
        self.source_dir = Path(source_dir)
        for file_path in self._get_files():
            print(f"Indexing file: {file_path}")
            self._index_file(file_path)
        print("Running worker")



if __name__ == '__main__':
    fire.Fire(Worker)