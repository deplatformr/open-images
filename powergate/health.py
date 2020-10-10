import os
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
powergate = PowerGateClient(api, False)
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

print(api)
print(ffs)


print("Checking node health...")
healthcheck = powergate.health.check()
print(healthcheck)
