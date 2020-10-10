from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks
import os

client = PowerGateClient("")

ffs = ""

token = ""

source_file = ""
current_path = os.getcwd()
upload_file = os.path.join(current_path, source_file)

defaultConfig = client.ffs.default_config(token)
print(defaultConfig)

iter = get_file_bytes(source_file)
res = client.ffs.stage(bytes_to_chunks(iter), token)
print(res)

push = client.ffs.push(res.cid, token)
print(push)

check = client.ffs.info(res.cid, token)
print(check)
