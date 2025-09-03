import sys
import os
import json
import time

# Add the parent directory to the Python path to allow imports from the main script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary functions and variables from the main login script
# This assumes your main script is named 'login.py' and is in the parent directory
from login import (
    login,
    getAuthCode,
    getAccessToken,
    getRefreshToken,
    make_request,
    OMADAC_ID,
    access_token # This is a global variable, so we need to be careful
)

def get_user_list(page, page_size, sorts=None, search_key=None):
    """
    Fetches a list of users from the Omada Controller.

    Args:
        page (int): The page number to retrieve, starting from 1.
        page_size (int): The number of users per page (1-1000).
        sorts (dict, optional): A dictionary for sorting, e.g., {'name': 'asc'}. Defaults to None.
        search_key (str, optional): A string to search for in user names. Defaults to None.

    Returns:
        dict: The 'result' part of the API response containing user data, or None on failure.
    """
    print("\n\n---- API Call: Get User List ----")
    if not access_token:
        print("\nMissing Access Token. Cannot get user list. Please log in first.")
        return None

    url_path = f"/openapi/v1/{OMADAC_ID}/users"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

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
    
    if response and response.json().get("errorCode") == 0:
        user_list_data = response.json().get("result", {})
        print("\nSuccessfully retrieved user list.")
        return user_list_data
    
    # Handle specific error from docs
    if response and response.json().get("errorCode") == -44118:
        print("Error: This interface only supports authorization code mode. Check your token.")

    return None

if __name__ == "__main__":
    # --- Step 1: Perform full login to get the access token ---
    print("--- Performing initial login to obtain access token ---")
    csrf, session = login()
    if not (csrf and session):
        print("Initial login failed. Exiting.")
    else:
        auth_code = getAuthCode()
        if not auth_code:
            print("Failed to get authorization code. Exiting.")
        else:
            # This will populate the global 'access_token' variable in the 'login' module
            getAccessToken() 

            if not access_token:
                print("Failed to get access token. Exiting.")
            else:
                # --- Step 2: Call the API function from this file ---
                user_list = get_user_list(page=1, page_size=10)
                if user_list:
                    print("\n--- User List Data ---")
                    print(json.dumps(user_list, indent=2))