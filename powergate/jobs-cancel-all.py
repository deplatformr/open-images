from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict
import os
import sqlite3

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, is_secure=False)

total_jobs = powergate.storage_jobs.summary(cids='', token=token)
total = MessageToDict(total_jobs)

try:
    executing = str(len(total["executingStorageJobs"]))
except:
    executing = "0"

try:
    queued = str(len(total["queuedStorageJobs"]))
except:
    queued = "0"

print(executing + " jobs currently executing.")
print(queued + " jobs currently queued.")

if executing != "0":
    print("Cancelling all executing jobs...")
    for job in total["executingStorageJobs"]:
        powergate.storage_jobs.cancel(job_id=job["id"], token=token)