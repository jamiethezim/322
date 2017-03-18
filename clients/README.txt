activate_user.py -> if the user not in the database, this client request creates a new user account. Otherwise, it updates their password and verifies them as active with accessibility to the features of the webservice.
revoke_user.py -> sets the user's accessibility to False, disabling them from accessing the features of the webservice.
