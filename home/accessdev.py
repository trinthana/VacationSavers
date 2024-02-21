class AccessDev:
   
    # Class variable
    base_url = "https://amt.accessdevelopment.com/api/v1/imports/"
    access_token = ""
    org_key = ""
    prg_key = ""


    @classmethod
    def calculate_sha256(cls, input_string):
        import hashlib
        
        # Convert the input string to bytes
        input_bytes = input_string.encode('utf-8')

        # Calculate the SHA-256 hash
        sha256_hash = hashlib.sha256(input_bytes).hexdigest()

        return sha256_hash
    
    @classmethod
    def import_access(cls, member, app):
        from django.contrib.auth.models import User
        from app.models import ApplicationToken, ApplicationChoices
        import requests, json

        url = cls.base_url
        access_token = cls.access_token
        org_key = cls.org_key
        prg_key = cls.prg_key

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
                    "organization_customer_identifier": org_key,
                    "program_customer_identifier": prg_key,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email,
                    "member_customer_identifier": user.username.upper(),  
                    "member_status": "OPEN",  
                }
                members.append(member_data)
            
            # Create the final JSON structure
            data = {
                "import": {
                    "members": members
                }
            }

            # Convert Python data to JSON text with indentation
            json_text = json.dumps(data, indent=2)

            headers = {
                "Accept": "application/json", 
                "Content-Type": "application/json",  
                "Access-Token": access_token,  
            }
           
            # Make the POST request with headers and JSON data
            response = requests.post(url, headers=headers, data=json_text)
        
            # Check if the request was successful (status code 2xx)
            if response.status_code // 100 == 2:
                #if success then put token back
                for user in user_list:
                    hash = org_key + "-" + prg_key + "-" + user.username.upper()
                    sha_text = cls.calculate_sha256(hash)

                    # Create a new ApplicationToken instance for the current user
                    application_token = ApplicationToken.objects.create(
                        user=user,
                        application=app,
                        token=sha_text
                    )
                
                return sha_text

            else:
                raise Exception("Error - " + response.text)
                return response.text
        else:
            raise Exception("User name is not found")
               
    def create_member(cls, member, app):
        from app.models import ApplicationChoices

        match app:
            case ApplicationChoices.ACCESSDEAL:
                AccessDev.access_token = 'b8849b6267be7df46d4642d5bbbb4bdc28d3bd9fc893abbf53f02a92a2ed26a1'
                AccessDev.org_key = "203700"
                AccessDev.prg_key = "203715"
                return cls.import_access(member, app)
            case ApplicationChoices.ACCESS:
                AccessDev.access_token = 'fb07e2dd9ea727a5d841272af97dfbace9174523eae21581362b330462e4f6d3'
                AccessDev.org_key = "203700"
                AccessDev.prg_key = "203736"
                return cls.import_access(member, app)
            case ApplicationChoices.ACCESSIFRAME:
                AccessDev.access_token = 'ca3f3acbaa6714057023aee3f5f8960eed66cfa216c5ab75afec2d7cb1679d82'
                AccessDev.org_key = "203700"
                AccessDev.prg_key = "203700"
                return cls.import_access(member, app)
            case _:
                return "No application provided"


