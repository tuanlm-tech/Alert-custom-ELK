from connections.elasticsearch_connection import es



users = es.security.get_user()

for username, info in users.items():
    print(f"\nUser: {username}")

    for role in info.get("roles", []):
        try:
            role_info = es.security.get_role(name=role)
            print(f"  Role: {role}")

            kibana = role_info[role].get("applications", [])
            for app in kibana:
                print(f"    App: {app.get('application')}")
                print(f"    Privileges: {app.get('privileges')}")

        except Exception as e:
            print(f"    Error loading role {role}: {e}")