import requests
import os
import shutil

download_dir = os.path.join(os.getcwd(), "source_data/segmentations")
urls = ("https://storage.googleapis.com/openimages/v5/train-masks/train-masks-0.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-1.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-2.zip")

for url in urls:

    split = os.path.split(url)
    file = split[1]
    filepath = os.path.join(download_dir, file)

    response = requests.get(url, stream=True, timeout=(3, 10))
    file = open(filepath, "wb")
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
