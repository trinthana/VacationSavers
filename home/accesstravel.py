class AccessTravel:
   
    # Class variable
    base_url = "https://auth.adcrws.com/api/v1/tokens"
    authorization_token = "ca3f3acbaa6714057023aee3f5f8960eed66cfa216c5ab75afec2d7cb1679d82"

    def get_session_token(cls, member, app):
        from django.contrib.auth.models import User
        import requests, json

        # Get all users which do not have Access Token yet.
        if len(member.username) > 0 :
            user_list = User.objects.filter(username=member.username)
        else :
            raise Exception("User name is blank")
            return ""        

        # Extract user data and format it in the desired structure
        if user_list.count() > 0 :
            members = []
            for user in user_list:
                member_data = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email,
                    "member_key": "VSID" + str(user.id).upper(),  
                    "scope": "travel",  
                }
                members.append(member_data)
            
            # Convert Python data to JSON text with indentation
            json_text = json.dumps(member_data, indent=2)

            headers = {
                "Accept": "application/json", 
                "Content-Type": "application/json",  
                "Authorization": "Bearer " + cls.authorization_token,  
            }
           
            # Make the POST request with headers and JSON data
            response = requests.post(cls.base_url, headers=headers, data=json_text)
        
            # Check if the request was successful (status code 2xx)
            if response.status_code // 100 == 2:
                data = response.json()
                session_token = data['session_token']
                print('Session Token:', session_token)
                return session_token

            else:
                raise Exception("Error - " + response.text)
                return response.text
        else:
            raise Exception("User name is not found")
