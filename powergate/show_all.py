import os
import sqlite3
import csv
from datetime import datetime
from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict


api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')


powergate = PowerGateClient(api, is_secure=True)

# get final storage deals info
cids = powergate.ffs.show_all(token=token)
