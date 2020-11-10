import ipfshttpclient
import sqlite3
import sys

def pin(package):
  client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
  # response = client.id()
    
  db = sqlite3.connect("open-images.sqlite")
  cursor = db.cursor()

  try:

    response = client.add(package)
    print(response["Hash'])  

    """
    response = client.pin.add(cid, timeout=50000)
    print("Pinning " + cid + "...")
    cursor.execute("UPDATE packages SET pinned = ? WHERE cid = ?", (True, cid),)
    db.commit()
    print("Successfully pinned.")
    """
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
