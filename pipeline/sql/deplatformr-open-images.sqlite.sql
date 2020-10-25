BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "labels" (
	"LabelName"	TEXT,
	"DisplayName"	TEXT,
	PRIMARY KEY("LabelName")
);
CREATE TABLE IF NOT EXISTS "trainable_labels" (
	"LabelName"	TEXT,
	PRIMARY KEY("LabelName")
);
CREATE TABLE IF NOT EXISTS "open_images" (
	"ImageID"	TEXT,
	"Subset"	TEXT,
	"OriginalURL"	TEXT,
	"OriginalLandingURL"	TEXT,
	"License"	TEXT,
	"AuthorProfileURL"	TEXT,
	"Author"	TEXT,
	"Title"	TEXT,
	"OriginalSize"	INTEGER,
	"OriginalMD5"	TEXT,
	"Thumbnail300KURL"	TEXT,
	"Rotation"	INTEGER,
	"created"	TEXT,
	"description"	TEXT,
	"mime_type"	TEXT,
	"width"	TEXT,
	"height"	TEXT,
	"resolution"	TEXT,
	"latitude"	TEXT,
	"longitude"	TEXT,
	"altitude"	TEXT,
	"filename"	TEXT,
	"package_name"	TEXT,
	"package_cid"	TEXT,
	"city"	,
	"country"	,
	PRIMARY KEY("ImageID")
);
CREATE TABLE IF NOT EXISTS "annotations" (
	"id"	INTEGER,
	"ImageID"	TEXT,
	"DisplayName"	TEXT,
	"Type"	TEXT,
	"Function"	TEXT,
	"Confidence"	INTEGER,
	"XMin1"	TEXT,
	"XMax1"	TEXT,
	"YMin1"	TEXT,
	"YMax1"	TEXT,
	"RelationshipLabel"	TEXT,
	"DisplayName2"	INTEGER,
	"XMin2"	TEXT,
	"XMax2"	TEXT,
	"YMin2"	TEXT,
	"YMax2"	TEXT,
	"isOccluded"	TEXT,
	"isTruncated"	TEXT,
	"isGroupOf"	TEXT,
	"isDepiction"	TEXT,
	"isInside"	TEXT,
	"MaskPath"	TEXT,
	"BoxID"	TEXT,
	"PredictedIoU"	TEXT,
	"Clicks"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "packages" (
	"name"	TEXT,
	"timestamp"	TEXT,
	"size"	INTEGER,
	"cid"	TEXT,
	"cid_timestamp"	TEXT,
	PRIMARY KEY("name")
);
COMMIT;
