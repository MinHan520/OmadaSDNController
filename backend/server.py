import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Add the project root to the Python path to allow imports from sdn_api
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'backend'))

from sdn_api import login as login_api
from sdn_api.login import getAuthCode, getAccessToken
from sdn_api.user import get_user_list

# --- Flask App Initialization ---
app = Flask(__name__)
# This enables CORS for all domains on all routes.
# For production, you might want to restrict this to your frontend's domain.
CORS(app)

# --- API Endpoints ---
@app.route('/api/users', methods=['GET'])
def api_get_users():
    """
    API endpoint to get a list of users.
    """
    if not login_api.access_token:
        return jsonify({"error": "Backend server not logged in to Omada.", "errorCode": -1}), 500

    # We call the existing function from user.py
    user_data = get_user_list(page=1, page_size=10)

    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "Failed to fetch users from Omada.", "errorCode": -1}), 500

def initial_login():
    """
    Performs the full login sequence to get the initial access token.
    """
    print("--- Performing initial server login to Omada Controller ---")
    csrf, session = login_api.login()
    if not (csrf and session):
        print("FATAL: Initial login failed. Cannot start server.", file=sys.stderr)
        return False
    
    auth_code = getAuthCode()
    if not auth_code:
        print("FATAL: Failed to get authorization code. Cannot start server.", file=sys.stderr)
        return False

    access_token, _ = getAccessToken()
    return bool(access_token)

if __name__ == '__main__':
    if initial_login():
        print("\n--- Backend server is ready and running on http://127.0.0.1:5000 ---")
        # The host='0.0.0.0' makes the server accessible from your local network
        app.run(host='0.0.0.0', port=5000, debug=True)