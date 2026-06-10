from connections.elasticsearch_connection import es

indices = es.cat.indices(format="json")

for idx in indices:
    print(
        f"""
INDEX   : {idx['index']}
HEALTH  : {idx['health']}
STATUS  : {idx['status']}
DOCS    : {idx['docs.count']}
SIZE    : {idx['store.size']}
-------------------------------
"""
    )