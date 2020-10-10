BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "labels" (
	"LabelName"	TEXT,
	"DisplayName"	TEXT,
	PRIMARY KEY("LabelName")
);
CREATE TABLE IF NOT EXISTS "train_labels_human" (
	"id"	INTEGER,
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	INTEGER,
	FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
	FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "test_labels_human" (
	"id"	INTEGER,
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	INTEGER,
	FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
	FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "validate_labels_human" (
	"id"	INTEGER,
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	INTEGER,
	FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
	FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "train_boxes" (
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	TEXT,
	"XMin"	TEXT,
	"XMax"	TEXT,
	"YMin"	TEXT,
	"YMax"	TEXT,
	"IsOccluded"	TEXT,
	"IsTruncated"	TEXT,
	"IsGroupOf"	TEXT,
	"IsDepiction"	TEXT,
	"IsInside"	TEXT,
	"XClick1X"	TEXT,
	"XClick2X"	TEXT,
	"XClick3X"	TEXT,
	"XClick4X"	TEXT,
	"XClick1Y"	TEXT,
	"XClick2Y"	TEXT,
	"XClick3Y"	TEXT,
	"XClick4Y"	TEXT
);
CREATE TABLE IF NOT EXISTS "test_boxes" (
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	TEXT,
	"XMin"	TEXT,
	"XMax"	TEXT,
	"YMin"	TEXT,
	"YMax"	TEXT,
	"IsOccluded"	TEXT,
	"IsTruncated"	TEXT,
	"IsGroupOf"	TEXT,
	"IsDepiction"	TEXT,
	"IsInside"	TEXT
);
CREATE TABLE IF NOT EXISTS "validate_boxes" (
	"ImageID"	TEXT,
	"Source"	TEXT,
	"LabelName"	TEXT,
	"Confidence"	TEXT,
	"XMin"	TEXT,
	"XMax"	TEXT,
	"YMin"	TEXT,
	"YMax"	TEXT,
	"IsOccluded"	TEXT,
	"IsTruncated"	TEXT,
	"IsGroupOf"	TEXT,
	"IsDepiction"	TEXT,
	"IsInside"	TEXT
);
CREATE TABLE IF NOT EXISTS "trainable_labels" (
	"LabelName"	TEXT,
	PRIMARY KEY("LabelName")
);
CREATE TABLE IF NOT EXISTS "test_segmentations" (
	"MaskPath"	TEXT,
	"ImageID"	TEXT,
	"LabelName"	TEXT,
	"BoxID"	TEXT,
	"BoxXMin"	TEXT,
	"BoxXMax"	TEXT,
	"BoxYMin"	TEXT,
	"BoxYMax"	TEXT,
	"PredictedIoU"	TEXT,
	"Clicks"	TEXT
);
CREATE TABLE IF NOT EXISTS "train_segmentations" (
	"MaskPath"	TEXT,
	"ImageID"	TEXT,
	"LabelName"	TEXT,
	"BoxID"	TEXT,
	"BoxXMin"	TEXT,
	"BoxXMax"	TEXT,
	"BoxYMin"	TEXT,
	"BoxYMax"	TEXT,
	"PredictedIoU"	TEXT,
	"Clicks"	TEXT
);
CREATE TABLE IF NOT EXISTS "validate_segmentations" (
	"MaskPath"	TEXT,
	"ImageID"	TEXT,
	"LabelName"	TEXT,
	"BoxID"	TEXT,
	"BoxXMin"	TEXT,
	"BoxXMax"	TEXT,
	"BoxYMin"	TEXT,
	"BoxYMax"	TEXT,
	"PredictedIoU"	TEXT,
	"Clicks"	TEXT
);
CREATE TABLE IF NOT EXISTS "train_relationships" (
	"ImageID"	TEXT,
	"LabelName1"	TEXT,
	"LabelName2"	TEXT,
	"XMin1"	TEXT,
	"XMax1"	TEXT,
	"YMin1"	TEXT,
	"YMax1"	TEXT,
	"XMin2"	TEXT,
	"XMax2"	TEXT,
	"YMin2"	TEXT,
	"YMax2"	TEXT,
	"RelationshipLabel"	TEXT
);
CREATE TABLE IF NOT EXISTS "test_relationships" (
	"ImageID"	TEXT,
	"LabelName1"	TEXT,
	"LabelName2"	TEXT,
	"XMin1"	TEXT,
	"XMax1"	TEXT,
	"YMin1"	TEXT,
	"YMax1"	TEXT,
	"XMin2"	TEXT,
	"XMax2"	TEXT,
	"YMin2"	TEXT,
	"YMax2"	TEXT,
	"RelationshipLabel"	TEXT
);
CREATE TABLE IF NOT EXISTS "validate_relationships" (
	"ImageID"	TEXT,
	"LabelName1"	TEXT,
	"LabelName2"	TEXT,
	"XMin1"	TEXT,
	"XMax1"	TEXT,
	"YMin1"	TEXT,
	"YMax1"	TEXT,
	"XMin2"	TEXT,
	"XMax2"	TEXT,
	"YMin2"	TEXT,
	"YMax2"	TEXT,
	"RelationshipLabel"	TEXT
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
	PRIMARY KEY("ImageID")
);
CREATE INDEX IF NOT EXISTS "train_images" ON "train_labels_human" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "train_labels" ON "train_labels_human" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "test_labels" ON "test_labels_human" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "validate_labels" ON "validate_labels_human" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "test_images" ON "test_labels_human" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "validate_images" ON "validate_labels_human" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "train_box_images" ON "train_boxes" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "train_box_label" ON "train_boxes" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "test_box_label" ON "test_boxes" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "validate_box_label" ON "validate_boxes" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "test_box_images" ON "test_boxes" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "validate_box_images" ON "validate_boxes" (
	"ImageId"
);
CREATE INDEX IF NOT EXISTS "validate_segmentation_image" ON "validate_segmentations" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "test_segmentation_image" ON "test_segmentations" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "train_segmentation_image" ON "train_segmentations" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "train_segmentation_label" ON "train_segmentations" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "validate_segmentation_label" ON "validate_segmentations" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "test_segmentation_label" ON "test_segmentations" (
	"LabelName"
);
CREATE INDEX IF NOT EXISTS "validate_relationship_image" ON "validate_relationships" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "test_relationship_image" ON "test_relationships" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "train_relationship_image" ON "train_relationships" (
	"ImageID"
);
CREATE INDEX IF NOT EXISTS "train_relationship_label1" ON "train_relationships" (
	"LabelName1"
);
CREATE INDEX IF NOT EXISTS "train_relationship_label2" ON "train_relationships" (
	"LabelName2"
);
CREATE INDEX IF NOT EXISTS "test_relationship_label2" ON "test_relationships" (
	"LabelName2"
);
CREATE INDEX IF NOT EXISTS "test_relationship_label1" ON "test_relationships" (
	"LabelName1"
);
CREATE INDEX IF NOT EXISTS "validate_relationship_label1" ON "validate_relationships" (
	"LabelName1"
);
CREATE INDEX IF NOT EXISTS "validate_relationship_label2" ON "validate_relationships" (
	"LabelName2"
);
COMMIT;
