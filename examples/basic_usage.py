"""
Initialize an access token at https://app.netlify.com/user/applications#personal-access-tokens

Then, run this example file from the root directory with:

$ NETLIFY_ACCESS_TOKEN=YOUR-ACCESS-TOKEN python examples/basic_usage.py
"""

import os
from pprint import pprint

from netlify import NetlifyClient

access_token = os.getenv("NETLIFY_ACCESS_TOKEN", "")

client = NetlifyClient(access_token=access_token)

pprint(client.get_current_user())
pprint(client.list_sites())
