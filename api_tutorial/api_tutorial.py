# Tutorial using Edge Fabric REST API's.

# author: Pratik Narode
# email: pratik.narode@macrometa.co

import base64
import json

import requests
import websocket

# Constants defined which are used throughout the tutorial.
FABRIC_URL = "https://fabric.macrometa.io"
FABRIC_NAME = "fabric"
ROOT_USER = "root"
ROOT_PWD = "poweruser"

TENANT_NAME = "tenant1"
TENANT_PWD = "tenantpwd"
GUEST_USER = "user1"
GUEST_PWD = "userpwd"
DB_NAME = "db1"
COLLECTION_NAME = "testcollection"
SUBSCRIPTION_NAME = "my-sub"

# Create a https session by passing username & password
session = requests.Session()
session.auth = (ROOT_USER, ROOT_PWD)

# Get list of regions where C8Fabric is running
url = FABRIC_URL + "/_database/_api/datacenter/all"
dcl_resp = session.get(url)
dcl_list = json.loads(dcl_resp.text)
regions = []
for dcl in dcl_list:
    dcl_url = dcl['tags']['url']
    regions.append(dcl_url)

# create tenant with tenant name and password
url = FABRIC_URL + "/_database/_api/tenant"
response = session.post(url,
                        json={
                            "extra": {},
                            "name": TENANT_NAME,
                            "passwd": TENANT_PWD
                        })

# Create guest user by passing in username and password
session = requests.Session()
session.auth = (ROOT_USER, ROOT_PWD)
session = requests.Session()
session.auth = (ROOT_USER, ROOT_PWD)
url = FABRIC_URL + "/_database/_tenant/{}/_db/_system/_admin/user".format(TENANT_NAME)
user = session.post(url=url, json={
    "active": True,
    "extra": {},
    "passwd": GUEST_PWD,
    "user": GUEST_USER

})

# Create a new real-time database ;
# Provide list of regions where the database should be replicated
# Assign permissions on the database to the guest user
session = requests.Session()
session.auth = (ROOT_USER, ROOT_PWD)
auth = session.post(FABRIC_URL)
url = FABRIC_URL + "/_database/_tenant/{}/_db/_system/_api/database".format(TENANT_NAME)
db = session.post(url, json={
    "name": DB_NAME,
    "options": {
        "dcList": regions,
        "realTime": True
    },
    "users": [
        {
            "active": True,
            "extra": {},
            "passwd": GUEST_PWD,
            "username": GUEST_USER
        }
    ]
})

# Create a test collection. collection type - 2 for document, 3 for edge
session = requests.Session()
session.auth = (GUEST_USER, GUEST_PWD)
auth = session.post(FABRIC_URL)
url = FABRIC_URL + "/_database/_tenant/{}/_db/{}/_api/collection".format(TENANT_NAME, DB_NAME)
col = session.post(url, json={
    "name": COLLECTION_NAME,
    "type": 2
})

# Using C8QL do CRUD operations on the collection.
session = requests.Session()
session.auth = (GUEST_USER, GUEST_PWD)
auth = session.post(FABRIC_URL)
url = FABRIC_URL + "/_database/_tenant/{}/_db/{}/_api/cursor".format(TENANT_NAME, DB_NAME)

# Read from the collection
col = session.post(url, json={
    "query": "FOR c IN testcollection RETURN c"  # Read from database
})

# Deleting from collection
col = session.post(url, json={
    "query": "FOR c IN testcollection REMOVE c IN testcollection"
})

# Create persistent global stream
url = FABRIC_URL + "/_tenant/{}/_db/{}/streams/persistent/stream/{}" \
    .format(TENANT_NAME, DB_NAME, "stream1")
user_session = requests.Session()
user_session.auth = (GUEST_USER, GUEST_PWD)
persistent_stream = user_session.post(url)

# Create non-persistent global stream
url = FABRIC_URL + "/_tenant/{}/_db/{}/streams/non-persistent/stream/{}" \
    .format(TENANT_NAME, DB_NAME, "stream1")
user_session = requests.Session()
user_session.auth = (GUEST_USER, GUEST_PWD)
non_persistent_stream = user_session.post(url)

# publish and subscribe messages to stream
# Publish message to a stream
TOPIC = 'wss://' + url + '/c8/_ws/ws/v2/producer/' + "persistent" + '/' + TENANT_NAME + '/' + FABRIC_NAME \
        + '.' + DB_NAME + '/' + "stream1"
ws = websocket.create_connection(TOPIC)
ws.send(json.dumps({
    'payload': base64.b64encode('Hello World'),
    'properties': {
        'key1': 'value1',
        'key2': 'value2'
    },
    'context': 5
}))
response = json.loads(ws.recv())
if response['result'] == 'ok':
    print('Message published successfully')
else:
    print('Failed to publish message:', response)
ws.close()

# Subscribe to a stream
TOPIC = 'wss://' + url + '/c8/_ws/ws/v2/consumer/' + "persistent" + '/' + TENANT_NAME + '/' + FABRIC_NAME \
        + '.' + DB_NAME + '/' + "stream1" + SUBSCRIPTION_NAME
ws = websocket.create_connection(TOPIC)
while True:
    msg = json.loads(ws.recv())
    if not msg: break

    print("received: {} - payload: {}".format(msg, base64.b64decode(msg['payload'])))
    # Acknowledge successful processing
    ws.send(json.dumps({'messageId': msg['messageId']}))

ws.close()

# delete tenant
session = requests.Session()
session.auth = (ROOT_USER, ROOT_PWD)
url = FABRIC_URL + "/_database/_api/tenant/{}".format(TENANT_NAME)
response = session.delete(url)
