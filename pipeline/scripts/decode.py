import base64
import hashlib

open_images_md5 = base64.b64decode("NPZ/DAcXUZLyM+AG2RgaOw==")

with open('source_data/images/rename.jpg', 'rb') as filehash:
    m = hashlib.md5()
    while True:
        data = filehash.read(8192)
        if not data:
            break
        m.update(data)

if m.hexdigest() == open_images_md5.hex():
    print("match made")
else:
    print("no match")
