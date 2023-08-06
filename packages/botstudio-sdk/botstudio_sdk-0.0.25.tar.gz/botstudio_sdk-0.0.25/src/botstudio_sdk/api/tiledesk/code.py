import requests


def _get_conversation_metadata(usename, password, project_id, request_id):
    """Get the converstaion metadata."""

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://api.tiledesk.com/v2/{project_id}/requests/{request_id}",
        headers=headers,
        auth=(usename, password),
    )
    return response.json()


def get_ga_client_id(username, password, project_id, requests_id):
    """Get the client id from the google analytics."""

    metadata = _get_conversation_metadata(username, password, project_id, requests_id)
    try:
        return metadata["lead"]["attributes"]["payload"]["clientId"]
    except KeyError:
        return "Unkown"


def check_tiledesk_api(username, password):
    """Check if the api is working."""
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "email": username,
        "password": password,
    }

    reponse = requests.post(
        f"https://api.tiledesk.com/v2/auth/signin",
        headers=headers,
        json=body,
    )
    if reponse.status_code == 200:
        return True
    else:
        return False


def close_converstation(username, password, project_id, request_id):
    """Close the converstaion."""
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.put(
        f"https://api.tiledesk.com/v2/{project_id}/requests/{request_id}/close",
        headers=headers,
        auth=(username, password),
    )
    return response.status_code


if __name__ == "__main__":
    import os

    USERNAME = os.getenv("API_TILEDESK_USERNAME")
    PASSWORD = os.getenv("API_TILEDESK_PASSWORD")
    # print(check_tiledesk_api(USERNAME, PASSWORD))

    _project_id = "6356af8679d534001a39bdf9"
    # _requests_id = "support-group-6356af8679d534001a39bdf9-9ef99fc770264658b45014259179e333"
    # _requests_id = "support-group-6356af8679d534001a39bdf9-1135c7e08e074616a3b6dcc114c9c7d8"
    # _requests_id = (
    #     "support-group-6356af8679d534001a39bdf9-d697319016694378a4ad00b9994ea03b"
    # )
    _requests_id ="support-group-6356af8679d534001a39bdf9-e8f94c9a4ed94aeda2399c817bf295a8"

    # print(_get_conversation_metadata(USERNAME, PASSWORD, _project_id, _requests_id))

    client_id = get_ga_client_id(USERNAME, PASSWORD, _project_id, _requests_id)
    print(client_id)
    closed = close_converstation(USERNAME, PASSWORD, _project_id, _requests_id)
    print(closed)
