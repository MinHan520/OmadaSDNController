import json

# Import from the sdn_api package
from .login import make_request

def _process_data_response(response):
    """Helper to process JSON responses from the Omada API."""
    if not response:
        return None, -1 # Generic error for no response

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")

        if error_code == 0:
            # On success, return the 'result' object and an error code of 0
            return response_data.get("result"), 0
        else:
            # On failure, return the full error payload and the specific error code
            return response_data, error_code
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None, -1 # Generic JSON error

def get_user_list(base_url, omadac_id, access_token, page, page_size, sorts=None, search_key=None):
    print("\n\n---- API Call: Get User List ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get user list.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users"
    headers = {"Authorization": f"AccessToken={access_token}"}
    params = {"page": page, "pageSize": page_size}

    if sorts:
        for key, value in sorts.items():
            params[f"sorts.{key}"] = value
    if search_key:
        params["searchKey"] = search_key

    response = make_request(base_url, "GET", url_path, headers=headers, params=params)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print("\nSuccessfully retrieved user list.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching user list: {error_msg} (Code: {error_code})")

    return data, error_code

# Get user Information
def get_user_info(base_url, omadac_id, access_token, user_id):
    """
    Fetches information for a single user from the Omada Controller.
    """
    print(f"\n\n---- API Call: Get User Info for ID: {user_id} ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get user info.")
        return None, -1

    if not user_id:
        print("\nUser ID cannot be empty.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users/{user_id}"
    headers = {"Authorization": f"AccessToken={access_token}"}

    response = make_request(base_url, "GET", url_path, headers=headers)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print(f"\nSuccessfully retrieved info for user {user_id}.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching user info: {error_msg} (Code: {error_code})")

    return data, error_code

def get_role_list(base_url, omadac_id, access_token):
    """
    Fetches a list of roles from the Omada Controller.
    """
    print("\n\n---- API Call: Get Role List ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get role list.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/roles"
    headers = {"Authorization": f"AccessToken={access_token}"}

    response = make_request(base_url, "GET", url_path, headers=headers)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print("\nSuccessfully retrieved role list.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching role list: {error_msg} (Code: {error_code})")

    return data, error_code

def get_role_info(base_url, omadac_id, access_token, role_id):
    """
    Fetches information for a single role from the Omada Controller.
    """
    print(f"\n\n---- API Call: Get Role Info for ID: {role_id} ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get role info.")
        return None, -1

    if not role_id:
        print("\nRole ID cannot be empty.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/roles/{role_id}"
    headers = {"Authorization": f"AccessToken={access_token}"}

    response = make_request(base_url, "GET", url_path, headers=headers)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print(f"\nSuccessfully retrieved info for role {role_id}.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching role info: {error_msg} (Code: {error_code})")

    return data, error_code

def get_local_users(base_url, omadac_id, access_token):
    """
    Fetches a list of local users (excluding owner) from the Omada Controller.
    """
    print("\n\n---- API Call: Get Local Users ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get local users.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users/local"
    headers = {"Authorization": f"AccessToken={access_token}"}

    response = make_request(base_url, "GET", url_path, headers=headers)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print("\nSuccessfully retrieved local users.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching local users: {error_msg} (Code: {error_code})")

    return data, error_code

def get_cloud_user(base_url, omadac_id, access_token):
    """
    Fetches a list of cloud users (excluding owner) from the Omada Controller.
    """
    print("\n\n---- API Call: Get Cloud Users ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get cloud users.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users/cloud"
    headers = {"Authorization": f"AccessToken={access_token}"}

    response = make_request(base_url, "GET", url_path, headers=headers)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print("\nSuccessfully retrieved cloud users.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error fetching cloud users: {error_msg} (Code: {error_code})")

    return data, error_code

def create_user(
    base_url,
    omadac_id,
    access_token,
    name,
    role_id,
    user_type,
    all_site,
    password=None,
    email=None,
    alert=None,
    incident_notification=None,
    sites=None,
    temporary_enable=None,
    start_time=None,
    end_time=None,
    _is_retry=False
):
    """
    Creates a new user on the Omada Controller.

    Args:     
        name (str): The username for the new user.
        role_id (str): The role ID to assign to the user.
        user_type (int): The type of user (0 for local, 1 for cloud).
        all_site (bool): Whether user has all site permission.
        password (str, optional): The password for the new user. Defaults to None.
        email (str, optional): The email for the new user. Defaults to None.
        alert (bool, optional): Whether to receive alert emails. Defaults to None.
        incident_notification (bool, optional): Whether to receive incident notifications. Defaults to None.
        sites (list, optional): List of site IDs for user privilege. Defaults to None.
        temporary_enable (bool, optional): Enable temporary worker permission. Defaults to None.
        start_time (int, optional): Validity start timestamp (ms). Defaults to None.
        end_time (int, optional): Validity end timestamp (ms). Defaults to None.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response, or None on failure.
    """
    print(f"\n\n---- API Call: Create User: {name} ----")
    if not access_token:
        print("\nMissing Access Token. Cannot create user.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users"

    headers = {
        "Authorization": f"AccessToken={access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "roleId": role_id,
        "type": user_type,
        "allSite": all_site,
    }

    # Add optional fields to the payload only if they are provided
    if password is not None: payload["password"] = password
    if email is not None: payload["email"] = email
    if alert is not None: payload["alert"] = alert
    if incident_notification is not None: payload["incidentNotification"] = incident_notification
    if sites is not None: payload["sites"] = sites
    if temporary_enable is not None: payload["temporaryEnable"] = temporary_enable
    if start_time is not None: payload["startTime"] = start_time
    if end_time is not None: payload["endTime"] = end_time

    response = make_request(base_url, "POST", url_path, headers=headers, json_data=payload)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print(f"\nSuccessfully created user '{name}'.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error creating user: {error_msg} (Code: {error_code})")

    return data, error_code

def modify_user(
    base_url,
    omadac_id,
    access_token,
    user_id,
    name,
    role_id,
    all_site,
    password=None,
    email=None,
    alert=None,
    force_modify=None,
    incident_notification=None,
    sites=None,
    temporary_enable=None,
    start_time=None,
    end_time=None,
    _is_retry=False
):
    """
    Modifies an existing user on the Omada Controller.

    Args:
        user_id (str): The ID of the user to modify.
        name (str): The new username for the user.
        role_id (str): The new role ID to assign to the user.
        all_site (bool): Whether user has all site permission.
        password (str, optional): The new password for the user. Defaults to None.
        email (str, optional): The new email for the user. Defaults to None.
        alert (bool, optional): Whether to receive alert emails. Defaults to None.
        force_modify (bool, optional): Force modify. Defaults to None.
        incident_notification (bool, optional): Whether to receive incident notifications. Defaults to None.
        sites (list, optional): List of site IDs for user privilege. Defaults to None.
        temporary_enable (bool, optional): Enable temporary worker permission. Defaults to None.
        start_time (int, optional): Validity start timestamp (ms). Defaults to None.
        end_time (int, optional): Validity end timestamp (ms). Defaults to None.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response, or None on failure.
    """
    print(f"\n\n---- API Call: Modify User: {user_id} ----")
    if not access_token:
        print("\nMissing Access Token. Cannot modify user.")
        return None, -1

    if not user_id:
        print("\nUser ID is required to modify a user.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users/{user_id}"

    headers = {
        "Authorization": f"AccessToken={access_token}",
        "Content-Type": "application/json"
    }

    payload = { "name": name, "roleId": role_id, "allSite": all_site }

    # Add optional fields to the payload only if they are provided
    if password is not None: payload["password"] = password
    if email is not None: payload["email"] = email
    if alert is not None: payload["alert"] = alert
    if force_modify is not None: payload["forceModify"] = force_modify
    if incident_notification is not None: payload["incidentNotification"] = incident_notification
    if sites is not None: payload["sites"] = sites
    if temporary_enable is not None: payload["temporaryEnable"] = temporary_enable
    if start_time is not None: payload["startTime"] = start_time
    if end_time is not None: payload["endTime"] = end_time

    response = make_request(base_url, "PUT", url_path, headers=headers, json_data=payload)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print(f"\nSuccessfully modified user '{name}' (ID: {user_id}).")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error modifying user: {error_msg} (Code: {error_code})")

    return data, error_code

def delete_user(base_url, omadac_id, access_token, user_id, force_delete=None):
    """
    Deletes an existing user from the Omada Controller.

    Args:
        user_id (str): The ID of the user to delete.
        force_delete (bool, optional): Force delete the user. Defaults to None.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: An empty dictionary on success, or None on failure.
    """
    print(f"\n\n---- API Call: Delete User: {user_id} ----")
    if not access_token:
        print("\nMissing Access Token. Cannot delete user.")
        return None, -1

    if not user_id:
        print("\nUser ID is required to delete a user.")
        return None, -1

    url_path = f"/openapi/v1/{omadac_id}/users/{user_id}"

    headers = {
        "Authorization": f"AccessToken={access_token}",
        "Content-Type": "application/json"
    }

    payload = {}
    if force_delete is not None:
        payload["forceDelete"] = force_delete

    response = make_request(base_url, "DELETE", url_path, headers=headers, json_data=payload if payload else None)
    data, error_code = _process_data_response(response)

    if error_code == 0:
        print(f"\nSuccessfully deleted user with ID: {user_id}.")
    else:
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else 'No response'
        print(f"Error deleting user: {error_msg} (Code: {error_code})")

    return data, error_code
