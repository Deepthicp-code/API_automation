import json
import sys
import requests
import argparse

# parse arguments
parser = argparse.ArgumentParser("user_authent_info_extractor.py")
parser.add_argument("email", help="The user email", type=str)
parser.add_argument("password", help="The user password", type=str)
args = parser.parse_args()

# API URL parts
URL = "https://app.fieldwire.com"
SIGN_IN_PATH = "/api/v3/sign_in"

# define a params dict for the parameters to be sent to the API
PARAMS = {'user_login': {'email': args.email, 'password': args.password}}
HEADERS = {'Fieldwire-Version': "2020-06-22",
           'Content-Type': "application/json"}

# send request
r = requests.post(URL + SIGN_IN_PATH, json=PARAMS, headers=HEADERS)

# extract data in json format
data = r.json()
if not "auth_token" in data:
    print("ERROR: no auth_token in {0}".format(data))
    sys.exit(-1)
if not "user" in data or not "id" in data["user"]:
    print("ERROR: no user nor id in {0}".format(data["user"]))
    sys.exit(-1)

# extract credentials
auth_token = data["auth_token"]
user_id = data["user"]["id"]

print("auth_token=" + auth_token)
print("user_id=" + str(user_id))


# make a verification call with credentials to make sure authentication works
print("")
print("verifying credentials...")
call_headers = HEADERS | {
    'Fieldwire-User-Id': str(user_id), 'Fieldwire-User-Token': auth_token}

# Show all projects in an account

resp = requests.get(
    "https://app.fieldwire.com/api/v3/account/projects",
    headers=call_headers)
assert (resp.status_code == 200), "Status code is not 200:" +\
    str(resp.status_code)
print("status_code="+str(resp.status_code))

# create new project
data = {"project": {"name": "test1"}}
resp = requests.post(url="https://app.fieldwire.com/api/v3/projects",
                     json=data,
                     headers=call_headers)
data = resp.json()
assert (resp.status_code == 201), "Status code is not 201:" +\
    str(resp.status_code)
assert data['name'] == 'test1', "user created with wrong name.expected:test but not found:" + \
    str(data['name'])
print(resp.text)
print(resp.json)
id = data["id"]
print("id="+str(id))

# get all projects
url = "https://app.fieldwire.com/api/v3/account/projects"
response = requests.get(url, headers=call_headers)
print(response.text)
print(response.json)


# creation of tasks
url = "https://app.fieldwire.com/api/v3/projects/318d7ebe-a361-4530-8238-edc39a54115d/tasks"
payload = {
    "id": "3f5085bb-5320-4b95-9c93-1d6a09118b10",
    "creator_user_id": 1195631,
    "last_editor_user_id": 1195631,
    "owner_user_id": 1195631,
    "floorplan_id": "3f5085bb-5320-4b95-9c93-1d6a09118b100",
    "location_id": "3f5085bb-5320-4b95-9c93-1d6a09118b10",
    "team_id": "3f5085bb-5320-4b95-9c93-1d6a09118b10",
    "Team": "new",
    "Location": "LA",
    "is_local": True,
    "name": "test",
    "due_date": "2022-09-11",
    "cost_value": 2,
    "man_power_value": 10,
    "pos_x": 1,
    "pos_y": 1,
    "priority": 1,
    "device_created_at": "2022-09-11T16:43:19.695Z",
    "device_updated_at": "2022-09-11T16:43:19.695Z",
    "due_at": "2022-09-11T16:43:19.695Z",
    "end_at": "2022-09-11T16:43:19.695Z",
    "fixed_at": "2022-09-11T16:43:19.695Z",
    "start_at": "2022-09-11T16:43:19.695Z",
    "verified_at": "2022-09-11T16:43:19.695Z",
    "status_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_ids": [1195631],
    "task_type_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
response = requests.post(url, json=payload, headers=call_headers)
print(response.text)
