import requests
import os
import shutil
from zipfile import ZipFile

download_dir = os.path.join(os.getcwd(), "source_data/segmentations")
urls = ("https://storage.googleapis.com/openimages/v5/train-masks/train-masks-0.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-1.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-2.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-3.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-4.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-5.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-6.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-7.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-8.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-9.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-a.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-b.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-c.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-d.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-e.zip",
        "https://storage.googleapis.com/openimages/v5/train-masks/train-masks-f.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-0.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-1.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-2.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-3.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-4.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-5.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-6.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-7.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-8.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-9.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-a.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-b.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-c.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-d.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-e.zip",
        "https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-f.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-0.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-1.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-2.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-3.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-4.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-5.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-6.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-7.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-8.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-9.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-a.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-b.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-c.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-d.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-e.zip",
        "https://storage.googleapis.com/openimages/v5/test-masks/test-masks-f.zip")

for url in urls:

    split = os.path.split(url)
    filename = split[1]
    filepath = os.path.join(download_dir, filename)

    response = requests.get(url, stream=True, timeout=(3, 10))
    file = open(filepath, "wb")
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)

    with ZipFile(filepath, 'r') as unzip_dir:
        unzip_dir.extractall(filename)

    os.remove(filepath)
