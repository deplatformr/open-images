from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks
import os

client = PowerGateClient("api.pow.deplatformr.textile.io:443", is_secure=True)

ffs = "8864a110-aa3c-45b4-be8d-28733952d12e"

token = "a8d61841-50e3-42dc-9c6a-09a51d5cde78"

source_file = "source_data/images/a12f879f459a5a2c.jpg"
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
