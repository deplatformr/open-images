from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict
import os
import sqlite3

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')

powergate = PowerGateClient(api, is_secure=False)

queued_jobs = powergate.storage_jobs.queued(cids='', token=token)
executing_jobs = powergate.storage_jobs.executing(cids='', token=token)

executing = MessageToDict(executing_jobs)
queued = MessageToDict(queued_jobs)

print(str(len(executing["storageJobs"])) + " jobs currently executing.")
print(str(len(queued["storageJobs"])) + " jobs currently queued.")


"""

cancel_job = powergate.admin.storage_jobs.cancel(user_id=user, cids=['3b84a9e2-c826-4b38-8144-9262665e8544]'])

print(cancel_job)

job_msg = powergate.admin.storage_jobs.executing(user_id=user, cids=['QmPTpqgybVctWdvxLP6VJP82bSfzz3hAh68zxeU9YU6npA'])

job = MessageToDict(job_msg)

print(job)
"""
