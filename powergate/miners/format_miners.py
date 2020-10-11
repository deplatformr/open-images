import csv

with open("excluded_miners.txt", "r") as miners_list:
    miners = miners_list.readlines()
    for miner in miners:
        split = miner.split(":")
        print('"' + split[0] + '",')
