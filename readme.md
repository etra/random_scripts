python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements


----
Reads from files defined in .env and writes to destination
`python extractor/build_json.py run dest 128.101.101.0 128.101.101.255`
Writes to ES (localhost:9200)
`python extractor/write_es.py run dest`