# API Documentation

**(add `'?format=json'` to end of all URLs)**

Note: if a `GET` or `POST` method is not indicated, then it doesn't exist for the given endpoint

# Users

1. `/api/v1/users/`

    `GET`: Return a list of users (requires authentication token and superuser permissions)

    Documentation:

        HTTP 200 OK
        Allow: GET, OPTIONS
        Content-Type: application/json
        Vary: Accept
        {
           "renders" : [
              "application/json",
              "text/html"
           ],
           "parses" : [
              "application/json",
              "application/x-www-form-urlencoded",
              "multipart/form-data"
           ],
           "description" : "",
           "name" : "User List"
        }

2. `/api/v1/users/login/`

    Documentation:

        HTTP 200 OK
        Allow: POST, OPTIONS
        Content-Type: application/json
        Vary: Accept
        {
            "name": "Login",
            "description": "Given a phone number, creates a `User` with that phone number, and then sends a text with a confirmation code. The `User` is **NOT** active (i.e. they can't do anything) until they get an authorization token, which is done via the next API endpoint.",
            "renders": [
                "application/json",
                "text/html"
            ],
            "parses": [
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data"
            ]
        }

    `POST` data:

        {
            "first_name": (REQUIRED; String),
            "last_name": (REQUIRED; String),
            "phone_number":  (REQUIRED; String in standard US phone format WITHOUT country code, dashes, or spaces)
        }

    Example `POST` request:

        {
            "first_name": "Adrian",
            "last_name": "Lineweaver",
            "phone_number": "6316559113"
        }

    Example `POST` result:

        HTTP 201 Created
        Allow: POST, OPTIONS
        Content-Type: application/json
        Vary: Accept

        {
            "first_name": "Adrian",
            "last_name": "Lineweaver",
            "phone_number": "6316559113"
        }

3. `/api/v1/users/api-token/`

    Documentation:

        HTTP 200 OK
        Allow: POST, OPTIONS
        Content-Type: application/json
        Vary: Accept

        {
            "name": "Token",
            "description": "Given a phone number and four-digit verification token (sent via text message), checks if the verification token is valid for the given phone number. If it is, it activates the `User` account and returns an authentication token to be used in all future API requests.",
            "renders": [
                "application/json",
                "text/html"
            ],
            "parses": [
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data"
            ]
        }

    Example `POST` request:

        {
            "phone_number": "6316559113",
            "auth_token": 1234
        }

    Example response:

        HTTP 201 Created
        Allow: POST, OPTIONS
        Content-Type: application/json
        Vary: Accept
        {
            "phone_number": "6316559113",
            "auth_token": "a546cb5f09119e780667e5e3dc315082899ffc43"
        }

    