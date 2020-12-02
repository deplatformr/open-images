import os
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, False)

print("Checking node health...")
healthcheck = powergate.health.check()
print(healthcheck)
