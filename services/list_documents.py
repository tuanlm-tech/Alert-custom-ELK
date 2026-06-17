from connections.elasticsearch_connection import es

INDEX_NAME = "kiosk-log-ssh_login-2026.06.15"

response = es.search(
    index=INDEX_NAME,
    size=10,
    query={
        "match_all": {}
    }
)

doc = response["hits"]["hits"][0]["_source"]

for field in doc.keys():
    print(field)