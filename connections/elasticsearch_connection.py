from elasticsearch import Elasticsearch


ELASTICSEARCH_HOST = "https://10.30.137.11:9200"
ELASTICSEARCH_USERNAME = "kiosk-siem"
ELASTICSEARCH_PASSWORD = "kiosk-siem"
es = Elasticsearch(
    ELASTICSEARCH_HOST,
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=False,
    ssl_show_warn=False
)

print(es.info())