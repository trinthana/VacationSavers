class Arrivia:
   
    # Class variable
    base_url = "https://api.saveonresorts.com/"
    api_usr = "Vacationsavers24"
    api_pwd = "iawdygcvqmndcqjt"

    @classmethod
    def create_account(cls, **kwargs):
        from app.forms import UserProfileForm
        from app.models import UserProfile, ApplicationChoices, ApplicationToken
        import requests, json
        from requests.structures import CaseInsensitiveDict
        from urllib.parse import urlencode

        #Create Default Account on Arrivia
        user = kwargs.get('user')

        #Create Arrivia Default Account
        current_user = user
        user_profile = UserProfile(user=user)

        user_data = json.dumps(
        {
            "Email":kwargs.get('email'),
            "Password":kwargs.get('password'),
            "FirstName":current_user.first_name,
            "LastName":current_user.last_name,
            "Address":user_profile.phone,
            "City":user_profile.city,
            "TwoLetterCountryCode":user_profile.country_code,
            "Phone":user_profile.phone,
            "ContractNumber":kwargs.get('username'),
            "UserAccountTypeID":5,
            "ReferringUserId":""
        }
        )

        url = cls.base_url + "v2/clubmembership/createdefault"
        api_usr = cls.api_usr
        api_pwd = cls.api_pwd

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["x-saveon-username"] = api_usr
        headers["x-saveon-secret"] = api_pwd

        # Make the POST request with headers and JSON data
        try:
            resp = requests.post(url, headers=headers, data=user_data)
        except requests.exceptions.ConnectionError: 
            return "Error", "Create User - Connection Refused", "", "", "", ""

        if resp['ResultType'] == 'success':
             # Create a new ApplicationToken instance for the current user
            application_token = ApplicationToken.objects.create(
                user=user,
                application=ApplicationChoices.ARRIVIA,
                token='',
                custom1=kwargs.get('email'),
                custom2=kwargs.get('password'),
                custom3=resp['Account']['UserId']
            )
            return "Success", "User is created in DB and Arrovia.", "", kwargs.get('email'), kwargs.get('password'), resp['Account']['UserId']
        else:
            return "Error", resp['Message'], "", "", "", ""
   
    @classmethod
    def get_token(cls, **kwargs):
        import requests, json
        from requests.structures import CaseInsensitiveDict
        from urllib.parse import urlencode

        url = cls.base_url + "clubmembership/getlogintoken"
        api_usr = cls.api_usr
        api_pwd = cls.api_pwd

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
    
        user_data = json.dumps({
            "APIUsername":api_usr,
            "APIPassword":api_pwd,
            "Email":kwargs.get('email'),
            "Password":kwargs.get('password'),
            "ContractNumber":""
        })
    
        try:
            resp = requests.post(url, headers=headers, data=user_data)
            return "Success", "Success", resp

        except requests.exceptions.ConnectionError: 
            return "Error", "Connection Refused", "Connection Refused"




