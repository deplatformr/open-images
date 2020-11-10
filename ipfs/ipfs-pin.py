import ipfshttpclient
import sqlite3
import sys

def pin(cid=None):
  client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
  # response = client.id()
    
  db = sqlite3.connect("pinned-packages.sqlite")
  cursor = db.cursor()

  if cid == None:
    cursor.execute("SELECT cid FROM packages WHERE cid IS NOT NULL AND pinned IS NULL LIMIT ?", (1,),)
    result = cursor.fetchone()
  
  try:
    response = client.pin.add(cid, timeout=50000)
    print("Pinning " + cid + "...")
    cursor.execute("UPDATE packages SET pinned = ? WHERE cid = ?", (True, cid),)
    db.commit()
    print("Successfully pinned.")

  except Exception as e:
    print(e)


if __name__ == '__main__':

    try:
        if sys.argv[1] is None:
            print("Please provide a CID.")
            sys.exit(0)
        else:
            pin(str(sys.argv[1]))
    except Exception as e:
        print("Unable to pin " + str(sys.argv[1]) + " to IPFS node.")
        print(e)
