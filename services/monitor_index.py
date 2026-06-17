from connections.elasticsearch_connection import es


def monitor_index(index_name):
    last_timestamp = None

    while True:
        query = {"match_all": {}}

        if last_timestamp:
            query = {
                "range": {
                    "@timestamp": {
                        "gt": last_timestamp
                    }
                }
            }

        response = es.search(
            index=index_name,
            size=1000,
            sort=[
                {"@timestamp": "asc"}
            ],
            query=query
        )

        hits = response["hits"]["hits"]

        for hit in hits:
            source = hit["_source"]

            print(source.get("message"))

            last_timestamp = source["@timestamp"]


if __name__ == "__main__":
    monitor_index("kiosk-log-ssh_login-2026.06.17")