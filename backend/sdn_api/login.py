import requests
import json

# --- Configuration ---
CLIENT_ID = "975fc957360942df99cbd661a833e4cc"
CLIENT_SECRET = "7488ee406c9843fa80e86d0f9570c693"
OMADAC_ID = "6efebeb06fb81dfe27d81641e734ada3"
# USERNAME = "admin"
# PASSWORD = "Admin@12345"

def make_request(base_url, method, url_path, headers=None, data=None, json_data=None,  params=None):
    """
    A stateless request helper that requires the base_url for each call.
    """
    if not base_url:
        raise ValueError("base_url must be provided to make_request")
    url = f"{base_url}{url_path}"
    print(f"\n--- New Request ---")
    print(f"Request: {method.upper()} {url}")
    if headers: print(f"Headers: {json.dumps(headers, indent=2)}")
    if params: print(f"Query Params: {json.dumps(params, indent=2)}")
    if json_data: print(f"JSON Body: {json.dumps(json_data, indent=2)}")
    if data: print(f"Form Data: {data}")

    try:
        # In production, you should use a valid certificate by setting verify=True
        # and possibly passing the path to your CA bundle.
        response = requests.request(
            method,
            url,
            headers=headers,
            data=data,
            json=json_data,
            params=params,
            verify=False
        )

        print(f"\n--- Response ---")
        print(f"Status Code: {response.status_code}")
        try:
            # Try to pretty-print JSON response
            print(f"Body: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            # Fallback for non-JSON response
            print(f"Body: {response.text}")

        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Step 1.1 : Login - Get CSRF Token and Session ID
def login_to_controller(base_url, username, password):
    print("\n---- Step 1: Logging in to get CSRF token and Session ID ----")
    # This endpoint is for the OpenAPI authorization flow, matching your curl command
    url_path = "/openapi/authorize/login"
    params = {
        "client_id": CLIENT_ID,
        "omadac_id": OMADAC_ID,
    }
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password
    }

    response = make_request(base_url, "POST", url_path, headers=headers, json_data=payload, params=params)

    if response:
        try:
            data = response.json()
            if data.get("errorCode") == 0:
                result = data.get("result", {})
                csrf_token = result.get("csrfToken")
                session_id = result.get("sessionId")
                print(f"\nSuccessfully logged in via OpenAPI.")
                print(f"CSRF Token: {csrf_token}")
                return csrf_token, session_id
            else:
                print(f"Login failed: {data.get('msg')}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from login response.")
    return None, None
 
# -- Step 1.2 : Get Authentication Code 
def get_auth_code(base_url, csrf_token, session_id):
    print("\n\n---- Step 2: Get Authentication Code ----")
    if not (csrf_token and session_id):
        print("\nMissing CSRF Token or SessionID. Please generate again later.")
        return None

    url_path = f"/openapi/authorize/code"
    params = {
        "client_id": CLIENT_ID,
        "omadac_id": OMADAC_ID,
        "response_type": "code"
    }
    headers ={
        "Content-Type": "application/json",
        "Csrf-token": csrf_token,
        "Cookie": f"TPOMADA_SESSIONID={session_id}"
    }

    response = make_request(base_url, "POST", url_path, headers=headers, params=params)
    if response:
        try:
            data = response.json()
            if data.get("errorCode") == 0:
                result = data.get("result", {})
                authorization_code = result
                print(f"\nSuccessfully retrieved authorization code.")
                print(f"Authorization Code: {result}")
                return authorization_code
            else:
                print(f"Failed to get authorization code: {data.get('msg')}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from getAuthCode response.")
    return None

# -- Step 1.3 : Get Access token 
def get_access_token(base_url, authorization_code):
    print("\n\n---- Step 3: Get Access Token ----")
    if not authorization_code:
        print("\nMissing Authorization Code. Cannot get access token.")
        return None, None
 
    url_path = "/openapi/authorize/token"
    params = {
        "grant_type": "authorization_code",
        "code": authorization_code
    }
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    header = {
        "Content-Type": "application/json"
    }
    
    response = make_request(base_url, "POST", url_path, headers=header, json_data=payload, params=params)
    if response:
        try:
            data = response.json()
            if data.get("errorCode") == 0:
                result = data.get("result", {})                 
                access_token = result.get("accessToken")
                refresh_token = result.get("refreshToken")
                print(f"\nSuccessfully retrieved access token.")
                print(f"Access Token: {access_token}")
                print(f"Refresh Token: {refresh_token}")
                return access_token, refresh_token
            else:
                print(f"Failed to get access token: {data.get('msg')}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from getAccessToken response.")
    return None, None
 
# -- Step 1.4 : Get Refresh token
def get_refresh_token(base_url, current_refresh_token):
    print("\n\n---- Step 4: Refreshing Access Token ----")
    if not current_refresh_token:
        print("\nMissing Refresh Token. Cannot get new access token.")
        return None, None

    url_path = "/openapi/authorize/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": current_refresh_token
    }
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    header = {
        "Content-Type": "application/json"
    }
    response = make_request(base_url, "POST", url_path, headers=header, json_data=payload, params=params)
    
    if response:
        try:
            data = response.json()
            if data.get("errorCode") == 0:
                result = data.get("result", {})                 
                new_access_token = result.get("accessToken")
                new_refresh_token = result.get("refreshToken")
                print(f"\nSuccessfully refreshed access token.")
                return new_access_token, new_refresh_token
            else:
                print(f"Failed to refresh access token: {data.get('msg')}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from getRefreshToken response.")
    return None, None