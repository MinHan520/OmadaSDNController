import sys
import os
import json
import time

# Add the project root ('OmadaSDNController') to the Python path.
# This allows us to import modules from anywhere in the project.
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Import from the sdn_api package
#from sdn_api import login as login_api
import login as login_api
from login import (
    getAuthCode,
    getAccessToken,
    getRefreshToken,
    make_request,
)

def _handle_expired_token_and_retry(func, *args, **kwargs):
    """
    Handles API token expiration by refreshing the token and retrying the original function call.

    Args:
        func (callable): The original API function to retry.
        *args: Positional arguments for the original function.
        **kwargs: Keyword arguments for the original function.

    Returns:
        The result of the retried function call, or None if token refresh fails.
    """
    print("Access token expired (errorCode: -44112). Attempting to refresh token...")
    new_access_token, _ = getRefreshToken()
    if new_access_token:
        print("Token refreshed successfully. Retrying the request...")
        kwargs['_is_retry'] = True
        return func(*args, **kwargs)
    else:
        print("Failed to refresh access token.")
        return None

### Need modification later 
# Get user list --> There will be method for us to sort thinsg up I need to change some part for this
def get_user_list(page, page_size, sorts=None, search_key=None, _is_retry=False):
    """
    Fetches a list of users from the Omada Controller.

    Args:
        page (int): The page number to retrieve, starting from 1.
        page_size (int): The number of users per page (1-1000).
        sorts (dict, optional): A dictionary for sorting, e.g., {'name': 'asc'}. Defaults to None.
        search_key (str, optional): A string to search for in user names. Defaults to None.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing user data, or None on failure.
    """
    print("\n\n---- API Call: Get User List ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get user list. Please log in first.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }
    # !!! Here can add on other params that are available in the get user list 
    params = {
        "page": page,
        "pageSize": page_size
    }
    
    if sorts:
        for key, value in sorts.items():
            params[f"sorts.{key}"] = value

    if search_key:
        params["searchKey"] = search_key

    response = make_request("GET", url_path, headers=headers, params=params)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        user_list_data = response_data.get("result", {})
        print("\nSuccessfully retrieved user list.")
        return user_list_data
    
    # Handle expired token error: -44112
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_user_list, page, page_size, sorts=sorts, search_key=search_key)

    if error_code == -44118:
        print("Error: This interface only supports authorization code mode. Check your token.")

    return None

# Get user Information
def get_user_info(user_id, _is_retry=False):
    """
    Fetches information for a single user from the Omada Controller.

    Args:
        user_id (str): The ID of the user to retrieve.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing user data, or None on failure.
    """
    print(f"\n\n---- API Call: Get User Info for ID: {user_id} ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get user info. Please log in first.")
        return None
    
    if not user_id:
        print("\nUser ID cannot be empty.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users/{user_id}"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }

    response = make_request("GET", url_path, headers=headers)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        user_info_data = response_data.get("result", {})
        print(f"\nSuccessfully retrieved info for user {user_id}.")
        return user_info_data
    
    # Handle expired token error: -44112
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_user_info, user_id)

    if error_code == -44118:
        print("Error: This interface only supports authorization code mode. Check your token.")

    print(f"Error fetching user info: {response_data.get('msg', 'Unknown error')}")
    return None

def get_role_list(_is_retry=False):
    """
    Fetches a list of roles from the Omada Controller.

    Args:
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing role data, or None on failure.
    """
    print("\n\n---- API Call: Get Role List ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get role list. Please log in first.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/roles"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }

    response = make_request("GET", url_path, headers=headers)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        role_list_data = response_data.get("result", {})
        print("\nSuccessfully retrieved role list.")
        return role_list_data
    
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_role_list)

    print(f"Error fetching role list: {response_data.get('msg', 'Unknown error')}")
    return None

def get_role_info(role_id, _is_retry=False):
    """
    Fetches information for a single role from the Omada Controller.

    Args:
        role_id (str): The ID of the role to retrieve.
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing role data, or None on failure.
    """
    print(f"\n\n---- API Call: Get Role Info for ID: {role_id} ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get role info. Please log in first.")
        return None
    
    if not role_id:
        print("\nRole ID cannot be empty.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/roles/{role_id}"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }

    response = make_request("GET", url_path, headers=headers)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        role_info_data = response_data.get("result", {})
        print(f"\nSuccessfully retrieved info for role {role_id}.")
        return role_info_data
    
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_role_info, role_id)

    print(f"Error fetching role info: {response_data.get('msg', 'Unknown error')}")
    return None

def get_local_users(_is_retry=False):
    """
    Fetches a list of local users (excluding owner) from the Omada Controller.

    Args:
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing local user data, or None on failure.
    """
    print("\n\n---- API Call: Get Local Users ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get local users. Please log in first.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users/local"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }

    response = make_request("GET", url_path, headers=headers)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        local_user_data = response_data.get("result", {})
        print("\nSuccessfully retrieved local users.")
        return local_user_data
    
    if error_code == -1004:
        print("\nThere are no user, please try again")
        return None

    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_local_users)

    print(f"Error fetching local users: {response_data.get('msg', 'Unknown error')}")
    return None

def get_cloud_user(_is_retry=False):
    """
    Fetches a list of cloud users (excluding owner) from the Omada Controller.

    Args:
        _is_retry (bool): Internal flag to prevent infinite retry loops.

    Returns:
        dict: The 'result' part of the API response containing cloud user data, or None on failure.
    """
    print("\n\n---- API Call: Get Cloud Users ----")
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot get cloud users. Please log in first.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users/cloud"
    
    headers = {
        "Authorization": f"AccessToken={login_api.access_token}"
    }

    response = make_request("GET", url_path, headers=headers)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        cloud_user_data = response_data.get("result", {})
        print("\nSuccessfully retrieved cloud users.")
        return cloud_user_data
    
    if error_code == -1004:
        print("\nThere are no user, please try again")
        return None

    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(get_cloud_user)

    print(f"Error fetching cloud users: {response_data.get('msg', 'Unknown error')}")
    return None

def create_user(
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
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot create user. Please log in first.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users"

    headers = {
        "Authorization": f"AccessToken={login_api.access_token}",
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

    response = make_request("POST", url_path, headers=headers, json_data=payload)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        create_user_result = response_data.get("result", {})
        print(f"\nSuccessfully created user '{name}'.")
        return create_user_result
    
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(
            create_user,
            name=name,
            role_id=role_id,
            user_type=user_type,
            all_site=all_site,
            password=password,
            email=email,
            alert=alert,
            incident_notification=incident_notification,
            sites=sites,
            temporary_enable=temporary_enable,
            start_time=start_time,
            end_time=end_time)

    print(f"Error creating user: {response_data.get('msg', 'Unknown error')}")
    return None

def modify_user(
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
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot modify user. Please log in first.")
        return None

    if not user_id:
        print("\nUser ID is required to modify a user.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users/{user_id}"

    headers = {
        "Authorization": f"AccessToken={login_api.access_token}",
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

    response = make_request("PUT", url_path, headers=headers, json_data=payload)
    
    if not response: return None
    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        modify_user_result = response_data.get("result", {})
        print(f"\nSuccessfully modified user '{name}' (ID: {user_id}).")
        return modify_user_result
    
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(modify_user, user_id=user_id, name=name, role_id=role_id, all_site=all_site, password=password, email=email, alert=alert, force_modify=force_modify, incident_notification=incident_notification, sites=sites, temporary_enable=temporary_enable, start_time=start_time, end_time=end_time)

    print(f"Error modifying user: {response_data.get('msg', 'Unknown error')}")
    return None

def delete_user(user_id, force_delete=None, _is_retry=False):
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
    if not login_api.access_token:
        print("\nMissing Access Token. Cannot delete user. Please log in first.")
        return None

    if not user_id:
        print("\nUser ID is required to delete a user.")
        return None

    url_path = f"/openapi/v1/{login_api.OMADAC_ID}/users/{user_id}"

    headers = {
        "Authorization": f"AccessToken={login_api.access_token}",
        "Content-Type": "application/json"
    }

    payload = {}
    if force_delete is not None:
        payload["forceDelete"] = force_delete

    response = make_request("DELETE", url_path, headers=headers, json_data=payload if payload else None)
    
    if not response:
        return None

    try:
        response_data = response.json()
        error_code = response_data.get("errorCode")
    except json.JSONDecodeError:
        if response.status_code in [200, 204]:
            print(f"\nSuccessfully deleted user with ID: {user_id}.")
            return {}
        print("Error: Failed to decode JSON from response.")
        return None

    if error_code == 0:
        print(f"\nSuccessfully deleted user with ID: {user_id}.")
        return response_data.get("result", {})
    
    if error_code == -44112 and not _is_retry:
        return _handle_expired_token_and_retry(delete_user, user_id=user_id, force_delete=force_delete)

    print(f"Error deleting user: {response_data.get('msg', 'Unknown error')}")
    return None
