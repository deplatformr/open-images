import os
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
powergate = PowerGateClient(api, False)
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

addresses = powergate.ffs.addrs_list(token)

print("ffs: " + ffs)
print("-----------")

for address in addresses.addrs:
    balance = powergate.wallet.balance(address.addr)
    print("name: " + address.name)
    print("address: " + address.addr)
    print("type: " + address.type)
    print("balance " + str(balance.balance))
