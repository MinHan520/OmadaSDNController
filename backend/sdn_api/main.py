import json

# Import from the sdn_api package
# Assuming login.py and user.py are in the same directory as main.py
import login as login_api
from login import (
    getAuthCode,
    getAccessToken,
    getRefreshToken,
)
from user import (
    get_user_list,
    get_user_info,
    get_role_list,
    get_role_info,
    get_local_users,
    get_cloud_user,
    create_user,
    modify_user,
    delete_user,
)


if __name__ == "__main__":
    # Step 1: Perform the initial login and get the first access token.
    csrf, session = login_api.login()
    if not (csrf and session):
        print("Initial login failed. Exiting.")
    else:
        auth_code = getAuthCode()
        if not auth_code:
            print("Failed to get authorization code. Exiting.")
        else:
            access_token, refresh_token = getAccessToken()

            if access_token and refresh_token:
                while True:
                    print("\n\n--- Main Menu ---")
                    print("1. Use Refresh Token to get a new Access Token")
                    print("2. User Management")
                    print("q. Quit")

                    try:
                        choice = input("Enter your choice: ").strip()

                        if choice == '1':
                            getRefreshToken()
                        elif choice == '2':
                            # User Management Top-Level Menu
                            while True:
                                print("\n\n--- User Management Menu ---")
                                print("1. User")
                                print("2. Roles")
                                print("b. Back to Main Menu")

                                mgmt_choice = input("Enter your choice: ").strip()

                                if mgmt_choice == '1':
                                    # User Sub-menu
                                    while True:
                                        print("\n\n--- User Menu ---")
                                        print("1. Get User List")
                                        print("2. Get User Info by ID")
                                        print("3. Get Local Users")
                                        print("4. Get Cloud Users")
                                        print("5. Create New User")
                                        print("6. Modify Existing User")
                                        print("7. Delete User")
                                        print("b. Back to User Management Menu")

                                        user_choice = input("Enter your choice: ").strip()

                                        if user_choice == '1':
                                            user_list = get_user_list(page=1, page_size=10)
                                            if user_list:
                                                print("\n--- User List Data (Page 1, Size 10) ---")
                                                print(json.dumps(user_list, indent=2))
                                        elif user_choice == '2':
                                            user_id_input = input("Enter the User ID to fetch (e.g., a client ID from the user list): ").strip()
                                            if user_id_input:
                                                user_info = get_user_info(user_id=user_id_input)
                                                if user_info:
                                                    print(f"\n--- User Info for ID: {user_id_input} ---")
                                                    print(json.dumps(user_info, indent=2))
                                        elif user_choice == '3':
                                            local_users = get_local_users()
                                            if local_users:
                                                print("\n--- Local User List ---")
                                                print(json.dumps(local_users, indent=2))
                                        elif user_choice == '4':
                                            cloud_users = get_cloud_user()
                                            if cloud_users:
                                                print("\n--- Cloud User List ---")
                                                print(json.dumps(cloud_users, indent=2))
                                        elif user_choice == '5':
                                            print("\n--- Create New User (fields with * are mandatory) ---")
                                            print("Tip: Use the 'Roles' menu to find a valid roleId first.")
                                            
                                            # --- Mandatory Inputs ---
                                            name = input("* Username: ").strip()
                                            role_id = input("* roleId {string}: ").strip()

                                            user_type = None
                                            while user_type is None:
                                                user_type_str = input("* Type (0=Local, 1=Cloud): ").strip()
                                                try:
                                                    user_type = int(user_type_str)
                                                    if user_type not in [0, 1]:
                                                        print("Invalid type. Please enter 0 or 1.")
                                                        user_type = None
                                                except ValueError:
                                                    print("Invalid input. Please enter a number (0 or 1).")

                                            all_site = None
                                            while all_site is None:
                                                all_site_str = input("* User has all site permissions? (y/n): ").strip().lower()
                                                if all_site_str == 'y':
                                                    all_site = True
                                                elif all_site_str == 'n':
                                                    all_site = False
                                                else:
                                                    print("Invalid input. Please enter 'y' or 'n'.")

                                            # --- Conditional Mandatory & Optional Inputs ---
                                            password = None
                                            if user_type == 0: # Local user
                                                password = input("* Password (8-128 chars, complex): ").strip()
                                                if not password:
                                                    print("\nPassword is mandatory for local users. Aborting.")
                                                    continue

                                            if not all([name, role_id]):
                                                print("\nUsername and roleId are mandatory. Aborting user creation.")
                                                continue

                                            print("\n--- Optional Fields (press Enter to skip) ---")
                                            email_input = input("Email: ").strip()
                                            email = email_input if email_input else None

                                            alert_input = input("Receive alert emails? (y/n): ").strip().lower()
                                            alert = True if alert_input == 'y' else False if alert_input == 'n' else None

                                            incident_input = input("Receive incident notifications? (y/n): ").strip().lower()
                                            incident_notification = True if incident_input == 'y' else False if incident_input == 'n' else None

                                            sites = None
                                            if not all_site:
                                                sites_input = input("Site privileges (comma-separated list of site IDs): ").strip()
                                                if sites_input:
                                                    sites = [s.strip() for s in sites_input.split(',')]

                                            temp_enable_input = input("Enable temporary worker permissions? (y/n): ").strip().lower()
                                            temporary_enable = True if temp_enable_input == 'y' else False if temp_enable_input == 'n' else None

                                            start_time, end_time = None, None
                                            if temporary_enable:
                                                start_time_input = input("Validity start time (timestamp in ms): ").strip()
                                                start_time = int(start_time_input) if start_time_input.isdigit() else None
                                                end_time_input = input("Validity end time (timestamp in ms): ").strip()
                                                end_time = int(end_time_input) if end_time_input.isdigit() else None

                                            # --- API Call ---
                                            result = create_user(
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
                                                end_time=end_time
                                            )
                                            if result:
                                                print("\n--- User Creation Result ---")
                                                print(json.dumps(result, indent=2))
                                        elif user_choice == '6':
                                            print("\n--- Modify Existing User (fields with * are mandatory) ---")
                                            print("Tip: Use 'Get User List' or 'Get User Info' to find the user ID and current values.")

                                            # --- Mandatory Inputs ---
                                            user_id = input("* User ID to modify: ").strip()
                                            if not user_id:
                                                print("\nUser ID is mandatory. Aborting.")
                                                continue
                                            
                                            name = input("* New Username: ").strip()
                                            role_id = input("* New roleId {string}: ").strip()

                                            all_site = None
                                            while all_site is None:
                                                all_site_str = input("* User has all site permissions? (y/n): ").strip().lower()
                                                if all_site_str == 'y':
                                                    all_site = True
                                                elif all_site_str == 'n':
                                                    all_site = False
                                                else:
                                                    print("Invalid input. Please enter 'y' or 'n'.")

                                            if not all([name, role_id]):
                                                print("\nUsername and roleId are mandatory. Aborting user modification.")
                                                continue

                                            print("\n--- Optional Fields (press Enter to skip, providing a value will update it) ---")
                                            
                                            password_input = input("New Password (leave blank to keep unchanged): ").strip()
                                            password = password_input if password_input else None

                                            email_input = input("New Email: ").strip()
                                            email = email_input if email_input else None

                                            alert_input = input("Receive alert emails? (y/n): ").strip().lower()
                                            alert = True if alert_input == 'y' else False if alert_input == 'n' else None

                                            force_modify_input = input("Force modify? (y/n): ").strip().lower()
                                            force_modify = True if force_modify_input == 'y' else False if force_modify_input == 'n' else None

                                            incident_input = input("Receive incident notifications? (y/n): ").strip().lower()
                                            incident_notification = True if incident_input == 'y' else False if incident_input == 'n' else None

                                            sites = None
                                            if not all_site:
                                                sites_input = input("Site privileges (comma-separated list of site IDs): ").strip()
                                                if sites_input:
                                                    sites = [s.strip() for s in sites_input.split(',')]

                                            temp_enable_input = input("Enable temporary worker permissions? (y/n): ").strip().lower()
                                            temporary_enable = True if temp_enable_input == 'y' else False if temp_enable_input == 'n' else None

                                            start_time, end_time = None, None
                                            if temporary_enable:
                                                start_time_input = input("Validity start time (timestamp in ms): ").strip()
                                                start_time = int(start_time_input) if start_time_input.isdigit() else None
                                                end_time_input = input("Validity end time (timestamp in ms): ").strip()
                                                end_time = int(end_time_input) if end_time_input.isdigit() else None

                                            # --- API Call ---
                                            result = modify_user(
                                                user_id=user_id, name=name, role_id=role_id, all_site=all_site,
                                                password=password, email=email, alert=alert, force_modify=force_modify,
                                                incident_notification=incident_notification, sites=sites,
                                                temporary_enable=temporary_enable, start_time=start_time, end_time=end_time
                                            )
                                            if result:
                                                print("\n--- User Modification Result ---")
                                                print(json.dumps(result, indent=2))
                                        elif user_choice == '7':
                                            print("\n--- Delete User ---")
                                            user_id_input = input("* User ID to delete: ").strip()
                                            if not user_id_input:
                                                print("\nUser ID is mandatory. Aborting.")
                                                continue

                                            force_delete_input = input("Force delete? (y/n, optional, press Enter to skip): ").strip().lower()
                                            force_delete = True if force_delete_input == 'y' else False if force_delete_input == 'n' else None

                                            # The delete_user function will print the success/failure message
                                            delete_user(user_id=user_id_input, force_delete=force_delete)
                                        elif user_choice.lower() == 'b':
                                            break
                                        else:
                                            print("\nInvalid choice. Please try again.")
                                elif mgmt_choice == '2':
                                    # Roles Sub-menu
                                    while True:
                                        print("\n\n--- Roles Menu ---")
                                        print("1. Get Role List")
                                        print("2. Get Role Info by ID")
                                        print("b. Back to User Management Menu")

                                        role_choice = input("Enter your choice: ").strip()
                                        if role_choice == '1':
                                            role_list = get_role_list()
                                            if role_list:
                                                print("\n--- Role List Data ---")
                                                print(json.dumps(role_list, indent=2))
                                        elif role_choice == '2':
                                            role_id_input = input("Enter the Role ID to fetch: ").strip()
                                            if role_id_input:
                                                role_info = get_role_info(role_id=role_id_input)
                                                if role_info:
                                                    print(f"\n--- Role Info for ID: {role_id_input} ---")
                                                    print(json.dumps(role_info, indent=2))
                                        elif role_choice.lower() == 'b':
                                            break
                                        else:
                                            print("\nInvalid choice. Please try again.")
                                elif mgmt_choice.lower() == 'b':
                                    break  # Go back to main menu
                                else:
                                    print("\nInvalid choice. Please try again.")
                        elif choice.lower() == 'q':
                            print("\nExiting script.")
                            break
                        else:
                            print("\nInvalid choice. Please try again.")
                    except KeyboardInterrupt:
                        print("\n\n--- Script interrupted by user. Exiting. ---")
                        break
            else:
                print("\nFailed to obtain initial tokens. Cannot proceed to interactive menu.")