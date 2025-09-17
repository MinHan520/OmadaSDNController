import sys
import os
import secrets
from flask import Flask, jsonify, request, session
from flask_cors import CORS

# Add the project root to the Python path to allow imports from sdn_api
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
 
from sdn_api import login as login_api
from sdn_api import user as user_api

# --- Flask App Initialization ---
app = Flask(__name__)
# A secret key is required for Flask session management
app.secret_key = secrets.token_hex(16)
# This enables CORS for all domains on all routes and allows credentials (cookies).
# For production, restrict this to your frontend's domain: CORS(app, origins="http://localhost:3000", supports_credentials=True)
CORS(app, supports_credentials=True)

# --- API Endpoints ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    ip_address = data.get('ipAddress')
    username = data.get('username')
    password = data.get('password')

    base_url = f"https://{ip_address}:8043"

    # --- Full login sequence ---
    print(f"--- Attempting login for user '{username}' on controller '{ip_address}' ---")
    csrf, session_id = login_api.login_to_controller(base_url, username, password)
    if not (csrf and session_id):
        return jsonify({"error": "Login Failed", "details": "Invalid credentials or controller unreachable."}), 401

    auth_code = login_api.get_auth_code(base_url, csrf, session_id)
    if not auth_code:
        return jsonify({"error": "Login Failed", "details": "Failed to get authorization code."}), 401

    access_token, refresh_token = login_api.get_access_token(base_url, auth_code)
    if not access_token:
        return jsonify({"error": "Login Failed", "details": "Failed to get access token."}), 401

    # --- Store tokens in the user's session ---
    session['omada_tokens'] = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'base_url': base_url,
        'omadac_id': login_api.OMADAC_ID
    }
    session.permanent = True # Make the session last longer

    print("--- Full login sequence successful, tokens stored in session ---")
    return jsonify({"success": True, "message": "Login successful."})

# --- API Endpoints ---
@app.route('/api/users', methods=['GET'])
def api_get_users():
    """
    API endpoint to get a list of users.
    """
    try:
        tokens = session.get('omada_tokens')
        if not tokens:
            return jsonify({"error": "Not authenticated. Please log in again.", "errorCode": -1}), 401

        # Initial call to get user list
        user_data, error_code = user_api.get_user_list(
            base_url=tokens['base_url'],
            omadac_id=tokens['omadac_id'],
            access_token=tokens['access_token'],
            page=1,
            page_size=10
        )

        # If token expired, refresh and retry
        if error_code == -44112: # Error code for expired token
            print("Access token expired. Attempting refresh...")
            new_access, new_refresh = login_api.get_refresh_token(tokens['base_url'], tokens['refresh_token'])

            if not new_access:
                session.pop('omada_tokens', None) # Clear session if refresh fails
                return jsonify({"error": "Session expired. Please log in again.", "errorCode": -1}), 401

            # Update session with new tokens and retry the call
            tokens['access_token'] = new_access
            tokens['refresh_token'] = new_refresh
            session['omada_tokens'] = tokens
            print("Token refreshed. Retrying original request...")

            user_data, error_code = user_api.get_user_list(
                base_url=tokens['base_url'],
                omadac_id=tokens['omadac_id'],
                access_token=tokens['access_token'],
                page=1,
                page_size=10
            )

        if error_code == 0:
            # The frontend expects the full object with errorCode and result
            return jsonify({"result": user_data, "errorCode": 0})
        else:
            error_msg = user_data.get('msg', 'Failed to fetch users from Omada.') if isinstance(user_data, dict) else "An unknown error occurred."
            return jsonify({"error": error_msg, "errorCode": error_code}), 500

    except Exception as e:
        print(f"An unexpected error occurred in /api/users: {e}", file=sys.stderr)
        return jsonify({"error": "An internal server error occurred.", "details": str(e), "errorCode": -1}), 500

if __name__ == '__main__':
    # The server now starts without an initial login.
    # Login is handled via the /api/login endpoint from the frontend.
    print("\n--- Backend server is ready and running on http://127.0.0.1:5000 ---")
    # use_reloader=False is helpful for development to avoid issues with state in global variables.
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    
    
