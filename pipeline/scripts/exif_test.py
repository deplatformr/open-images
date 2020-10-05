import exifread
import os

images = os.listdir("source_data/images/100 metres hurdles/") 

for image in images:
# Open image file for reading (binary mode)
    f = open("source_data/images/100 metres hurdles/" + image, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote', 'EXIF UserComment'):
            print(tag + ": ", tags[tag])

    print("-------")


#gps = str(tags["GPS GPSLatitude"])
#print(gps[0])
