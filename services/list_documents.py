from connections.elasticsearch_connection import es

INDEX_NAME = "kiosk-log-cisco_log-2026.06.05"

response = es.search(
    index=INDEX_NAME,
    size=10,
    query={
        "match_all": {}
    }
)

for hit in response["hits"]["hits"]:

    print("ID:", hit["_id"])
    print("SOURCE:", hit["_source"])
    print("----------------------------")