import operator
import json

cheap_working_miners = {}

# Get Miner IDs for functioning miners
with open("functioning_miners.txt", "r") as miners_list:
    miners = miners_list.readlines()
    for miner in miners:
        split = miner.split(":")
        cheap_working_miners[split[0]] = None

# Get ask prices from miners
with open("miner_asks.txt", "r") as miners_list:
    lines = miners_list.readlines()
    lines_length = len(lines)
    for i in range(0, lines_length):
        if lines[i][:4] == "Ask:":
            # Make sure miner can accomodate 1 GiB+ packages
            if lines[i + 3] == "Max Piece size: 1 MiB\n":
                continue
            split = lines[i].split(" ")
            miner = split[1][:-1]
            split = lines[i + 1].split(": ")
            price = split[1][:-5]
            if miner in cheap_working_miners:
                cheap_working_miners[miner] = price

# Match functioning miners list to ask price list
pop_list = []
for key, value in cheap_working_miners.items():
    if cheap_working_miners[key] == None:
        pop_list.append(key)
for empty_value in pop_list:
    cheap_working_miners.pop(empty_value)
sorted_miners = sorted(cheap_working_miners.items(),
                       key=operator.itemgetter(1))

# Print ranked list
for i in range(0, len(sorted_miners)):
    print(str(i + 1) + ". " + sorted_miners[i]
          [0] + ": " + sorted_miners[i][1] + " FIL")

# Set maximum client price for storage deals
maximum_price = 0.0000000005

miners = []
for miner in sorted_miners:
    if float(miner[1]) <= maximum_price:
        miners.append(miner[0])

# Print miners.json
cheap_miners = {}
cheap_miners = (
    {"buckets": [{"name": "cheapMiners", "amount": 5, "minerAddresses": miners}]})

with open("miners.json", "w", encoding="utf-8") as outfile:
    json.dump(cheap_miners, outfile, indent=4, ensure_ascii=False)
