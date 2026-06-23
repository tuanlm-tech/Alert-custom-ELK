from connections.elasticsearch_connection import es


def get_users():
    users = es.security.get_user()

    result = []

    for username, info in users.items():
        result.append({
            "username": username,
            "roles": info.get("roles", []),
            "enabled": info.get("enabled")
        })

    return result


def get_roles():
    roles = es.security.get_role()

    return list(roles.keys())


def get_current_user():
    auth = es.security.authenticate()

    return {
        "username": auth.get("username"),
        "roles": auth.get("roles")
    }