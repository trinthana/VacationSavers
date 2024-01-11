from django.contrib.auth.models import User
from app.models import ApplicationToken, ApplicationChoices, PackageChoices
from django.http import JsonResponse
import requests, json, hashlib

def calculate_sha256(input_string):
    # Convert the input string to bytes
    input_bytes = input_string.encode('utf-8')

    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()

    return sha256_hash

def import_access_travel(member):
    url = "https://amt.accessdevelopment.com/api/v1/imports/"
    access_token = 'fb07e2dd9ea727a5d841272af97dfbace9174523eae21581362b330462e4f6d3'
    org_key = "203700"
    prg_key = "203736"

    # Get all users which do not have Access Token yet.
    if member is not None and member != '' :
        user_list = User.objects.filter(user=member)
    
    else :
        user_list = User.objects.exclude(
            applicationtoken__application = ApplicationChoices.ACCESS
        )
    
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
                hash = org_key + "-" + prg_key + user.username.upper()
                sha_text = calculate_sha256(hash)

                # Create a new ApplicationToken instance for the current user
                application_token = ApplicationToken.objects.create(
                    user=user,
                    application=ApplicationChoices.ACCESS,
                    token=sha_text
                )
            
            return response.json()

        else:
            return response.json()

def import_access_deals(member):
    url = "https://amt.accessdevelopment.com/api/v1/imports/"
    access_token = 'b8849b6267be7df46d4642d5bbbb4bdc28d3bd9fc893abbf53f02a92a2ed26a1'
    org_key = "203700"
    prg_key = "203715"

    # Get all users which do not have Access Token yet.
    if member is not None and member != '' :
        user_list = User.objects.filter(user=member)
    
    else :
        user_list = User.objects.exclude(
            applicationtoken__application = ApplicationChoices.ACCESSDEAL
        )
    
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
                hash = org_key + "-" + prg_key + user.username.upper()
                sha_text = calculate_sha256(hash)

                # Create a new ApplicationToken instance for the current user
                application_token = ApplicationToken.objects.create(
                    user=user,
                    application=ApplicationChoices.ACCESSDEAL,
                    token=sha_text
                )
            
            return response.json()

        else:
            return response.json()

def import_access_iframe(member):
    url = "https://amt.accessdevelopment.com/api/v1/imports/"
    access_token = 'ca3f3acbaa6714057023aee3f5f8960eed66cfa216c5ab75afec2d7cb1679d82'
    org_key = "203700"
    prg_key = "203700"

    # Get all users which do not have Access Token yet.
    if member is not None and member != '' :
        user_list = User.objects.filter(user=member)
    
    else :
        user_list = User.objects.exclude(
            applicationtoken__application = ApplicationChoices.ACCESSIFRAME
        )
    
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
                hash = org_key + "-" + prg_key + user.username.upper()
                sha_text = calculate_sha256(hash)

                # Create a new ApplicationToken instance for the current user
                application_token = ApplicationToken.objects.create(
                    user=user,
                    application=ApplicationChoices.ACCESSIFRAME,
                    token=sha_text
                )
            
            return response.json()

        else:
            return response.json()

def import_access_member(member):

    ret1 = import_access_travel('')
    ret2 = import_access_deals('')
    ret3 = import_access_iframe('')

    if  ret1 is not None :
        dictA = json.loads(ret1)
    else :
        dictA = {}

    if  ret2 is not None :
        dictB = json.loads(ret2)
    else :
        dictB = {}
    
    if  ret3 is not None :
        dictC = json.loads(ret3)
    else :
        dictC = {}

    merged_dict = dictA.copy()
    merged_dict.update(dictB)
    merged_dict.update(dictC)
    
    return json.dumps(merged_dict)


