import ipfshttpclient
import sqlite3
import sys
import os

def pin(package):
  client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
  # response = client.id()

  db = sqlite3.connect("pinned-packages.sqlite")
  cursor = db.cursor()

  try:

    print("Adding " + package + " to IPFS...")
    response = client.add(package)
    cid = response["Hash"]

    print("Pinning " + cid)
    response = client.pin.add(cid, timeout=50000)
    cursor.execute("UPDATE packages SET pinned = ? WHERE cid = ?", (True, cid),)
    db.commit()

    print("Successfully added and pinned to IPFS.")
    print("Deleting source file.")
    os.remove(package)

  except Exception as e:
    print(e)


if __name__ == '__main__':

    path = "/media/ipfsnode/tmp/deplatformr-open-images-"
    start_package = 134
    end_package = 169

    for i in range(start_package, end_package):
        package_path = path + i + ".tar"
        pin(package_path)