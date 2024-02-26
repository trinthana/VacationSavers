class Arrivia:
   
    # Class variable
    base_url = "api.saveonresorts.com"
    api_usr = "Vacationsavers24"
    api_pwd = "iawdygcvqmndcqjt"

    @classmethod
    def create_account(cls, **kwargs):
        from app.forms import UserProfileForm
        from app.models import UserProfile, ApplicationChoices, ApplicationToken
        import requests, json
        from requests.structures import CaseInsensitiveDict
        from urllib.parse import urlencode
        import http.client
        from urllib.error import HTTPError
        from django.contrib.auth.models import User

        #Create Default Account on Arrivia
        user = kwargs.get('user')

        #Create Arrivia Default Account
        current_user = user
        #user_profile = UserProfile(user=user)
        user_profile = UserProfile.objects.get(user__username=current_user)

        user_data = json.dumps(
        {
            "Email":kwargs.get('email'),
            "Password":kwargs.get('password'),
            "FirstName":current_user.first_name,
            "LastName":current_user.last_name,
            "Address":user_profile.address,
            "City":user_profile.city,
            "TwoLetterCountryCode":user_profile.country_code,
            "Phone":user_profile.phone,
            "ContractNumber":'VS'+kwargs.get('username'),
            "UserAccountTypeID":5,
            "ReferringUserId":""
        }
        )

        url = "/v2/clubmembership/createdefault"
        api_usr = cls.api_usr
        api_pwd = cls.api_pwd

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Accept-Type"] = "application/json"
        headers["x-saveon-username"] = api_usr
        headers["x-saveon-secret"] = api_pwd

        # Make the POST request with headers and JSON data
        try:
            conn = http.client.HTTPSConnection(cls.base_url)
            conn.request("POST", url, user_data, headers)
            resp = conn.getresponse()
            data = json.loads(resp.read())
        except HTTPError as err:
            raise Exception(data)
            #return "Error", "", "", "", "", ""

        if data['ResultType'] == 'success':
             # Create a new ApplicationToken instance for the current user
            application_token = ApplicationToken.objects.create(
                user=user,
                application=ApplicationChoices.ARRIVIA,
                token='',
                custom1=kwargs.get('email'),
                custom2=kwargs.get('password'),
                custom3=data['Account']['UserId']
            )
            return "Success", "User is created in DB and Arrovia.", "", kwargs.get('email'), kwargs.get('password'), data['Account']['UserId']
        else:
            return "Error", data['Message'], "", "", "", ""
   
    @classmethod
    def get_token(cls, **kwargs):
        import requests, json
        from requests.structures import CaseInsensitiveDict
        from urllib.parse import urlencode
        import http.client
        from urllib.error import HTTPError

        url = "/clubmembership/getlogintokennovalidation"
        api_usr = cls.api_usr
        api_pwd = cls.api_pwd

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Accept-Type"] = "application/json"
    
        user_data = json.dumps({
            "APIUsername":api_usr,
            "APIPassword":api_pwd,
            "Email":kwargs.get('email'),
            "Password":kwargs.get('password'),
            "ContractNumber":'VS'+kwargs.get('username')
        })

        try:
            conn = http.client.HTTPSConnection(cls.base_url)
            conn.request("POST", url, user_data, headers)
            resp = conn.getresponse()
            data = resp.read().decode('utf-8').replace('"', '')
            # Split the string by colon (":")
            if ':' in data:
                # Extract the token which is the second part after the colon
                parts = data.split(':')
                token = parts[1].strip()
            else:
                token = data

            return "Success", "Success", token

        except HTTPError as err: 
            return "Error", "Connection Refused", HTTPError




