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

    print("Pinning " + cid + "...")
    response = client.pin.add(cid, timeout=50000)
    cursor.execute("UPDATE packages SET pinned = ? WHERE cid = ?", (True, cid),)
    db.commit()

    print("Successfully added and pinned to IPFS.")
    print("Deleting source file.")
    os.remove(package)

  except Exception as e:
    print(e)


if __name__ == '__main__':

    try:
        if sys.argv[1] is None:
            print("Please provide a package name.")
            sys.exit(0)
        else:
            pin(str(sys.argv[1]))
    except Exception as e:
        print("Unable to add " + str(sys.argv[1]) + " to IPFS node.")
        print(e)
