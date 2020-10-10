import os
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
powergate = PowerGateClient(api, False)
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

defaultConfig = powergate.ffs.default_config(token)
print(defaultConfig)

print("Loading new default config...")
with open("config_deplatformr.slingshot_1.json", "r") as f:
    config = f.read()

powergate.ffs.set_default_config(config, token)

defaultConfig = powergate.ffs.default_config(token)
print("Updated default config:")
print(defaultConfig)
