Permanent photos availability on Flickr is not guaranteed. See https://www.archiveteam.org/index.php?title=Flickr

Dataset metadata is scattered across several large CSV files. They are not aggregated per photo. Metadata is not "inextricably linked" to the source material. Hosted at https://storage.googleapis.com/openimages/web/download.html

Created a schema.org/ImageObject based JSON-LD profile for the photographs in the Open Images dataset, now making their metadata accessible as Linked Open Data.

Create an unofficial URN namespace format for Open Image IDs ("openimage:<ImageID>")

Extracted extra contextual information from the photographs: creation data, description, mime type, height, length, resolution, latitude, longitude, altitude.

The provided MD5 hash of the original JPEG-encoded images were base64 encoded. The hashes needed to be decoded and converted to Hex format to make them usable.

The segmentation files were stored seperately from their source files and CSV metadata. The are now stored them with their source file in the same archival package and JSON-LD metadata.

Created self-describing 4 GiB maximum packages of photographs for backup to Filecoin using the OCFL and Bagit.

NOTES
-----
* The Complete Open Images set (version 6) has 9,178,275 images. 

* Annotation data includes labels, boxes, segmentations and relationships (the train, validate and test sets for each). 

* Label annotations only include those that were human-verified (7,337,077 images).

* Localized Narratives were not included. 

* Image ids are generated based on hashes of the data so effectively the sampling within a stratum is pseudo-random and deterministic. It is not indicated what hashes were used>

* Thumbnails are not standardized and not included. URL to thumbnail file is provided.

"Thumbnail300KURL is an optional URL to a thumbnail with ~300K pixels (~640x480). 300K: Images have roughly 300,000 pixels. JPEG quality of 72. It is provided for the convenience of downloading the data in the absence of more convenient ways to get the images. If missing, OriginalURL must be used (and then resized to the same size, if needed). These thumbnails are generated on the fly and their contents and even resolution might be different every day."" 

* There is a surprisingly high number of 404 and 410 failure responses from the Flickr servers hosting the images. I used a very high timeout setting of 3 seconds for connection and 10 seconds for reading to minimize server/network bottleneck issues.

From a Google representative: "We (Google) do not host the images themselves, we just annotated them, and host the annotations and links to images. The images cannot be retrieved anymore if the authors removed them. Five percent of Open Images missing from Flickr actually sounds too low.

BTW, the subset of images that's annotated with bounding boxes (1.9 Million) is hosted in full by CVDF or Arpen."

* The original images, JSON-LD sidecar file and related segmentation files are bundled into tarball packages that are a maximum of 4 GiB in size (to comply with current Filecoin recommendations and Powergate restrictions). Note that compression has not been applied but the tarballs may be smaller than the sum of the files they contain due to the fact that tar can reduce space usage when used on a large number of small files that are smaller than the filesystem's cluster size. For example, if a filesystem uses 1kb clusters, even a file that contains a single byte will consume 1kb (plus an inode). A tar archive file does not have this overhead.