from pygate_grpc.client import PowerGateClient
import os

# Connect to Powergate
api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')
powergate = PowerGateClient(api, is_secure=False)

cid = 'QmZgRCFJEBjHFbqzGeVHSM5S1zjB5b14XenPPbRzsMf3vj'

powergate.config.apply(cid, override=True, token=token)