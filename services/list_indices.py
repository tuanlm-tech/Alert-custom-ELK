# import time

# from connections.elasticsearch_connection import es

# INDEX_NAME = "kiosk-log-ssh_login-2026.06.19"

# last_timestamp = None

# # Lưu thời điểm cuối cùng đã xử lý message
# message_cache = {}

# while True:
#     try:
#         query = {"match_all": {}}

#         if last_timestamp:
#             query = {
#                 "range": {
#                     "@timestamp": {
#                         "gt": last_timestamp
#                     }
#                 }
#             }

#         response = es.search(
#             index=INDEX_NAME,
#             size=1000,
#             sort=[
#                 {"@timestamp": "asc"}
#             ],
#             query=query
#         )

#         hits = response["hits"]["hits"]

#         current_time = time.time()

#         # Xóa các message đã quá 3 giây
#         expired_keys = [
#             key
#             for key, timestamp in message_cache.items()
#             if current_time - timestamp > 3
#         ]

#         for key in expired_keys:
#             del message_cache[key]

#         for hit in hits:
#             source = hit["_source"]

#             message = source.get("message", "")
#             timestamp = source.get("@timestamp")

#             # Bỏ qua nếu message đã xuất hiện trong vòng 3 giây
#             if message in message_cache:
#                 last_timestamp = timestamp
#                 continue

#             print(message)

#             # Đánh dấu thời gian xử lý
#             message_cache[message] = current_time

#             last_timestamp = timestamp

#         time.sleep(1)

#     except Exception as e:
#         print(f"Error: {e}")
#         time.sleep(5)