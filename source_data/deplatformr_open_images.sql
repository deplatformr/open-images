CREATE TABLE IF NOT EXISTS "labels" (
    "LabelName" TEXT,
    "DisplayName"   TEXT,
    PRIMARY KEY("LabelName")
);
CREATE TABLE IF NOT EXISTS "train_labels_human" (
    "id"    INTEGER,
    "ImageID"   TEXT,
    "Source"    TEXT,
    "LabelName" TEXT,
    "Confidence"    INTEGER,
    FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
    FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
    PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "test_labels_human" (
    "id"    INTEGER,
    "ImageID"   TEXT,
    "Source"    TEXT,
    "LabelName" TEXT,
    "Confidence"    INTEGER,
    FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
    FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
    PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "validate_labels_human" (
    "id"    INTEGER,
    "ImageID"   TEXT,
    "Source"    TEXT,
    "LabelName" TEXT,
    "Confidence"    INTEGER,
    FOREIGN KEY("LabelName") REFERENCES "labels"("LabelName"),
    FOREIGN KEY("ImageID") REFERENCES "open_images"("ImageID"),
    PRIMARY KEY("id")
);
CREATE INDEX train_images ON train_labels_human (ImageId);
CREATE INDEX train_labels ON train_labels_human (LabelName);
CREATE INDEX test_labels ON test_labels_human (LabelName);
CREATE INDEX validate_labels ON validate_labels_human (LabelName);
CREATE INDEX test_images ON test_labels_human (ImageId);
CREATE INDEX validate_images ON validate_labels_human (ImageId);
CREATE TABLE IF NOT EXISTS "open_images" (
    "ImageID"   TEXT,
    "Subset"    TEXT,
    "OriginalURL"   TEXT,
    "OriginalLandingURL"    TEXT,
    "License"   TEXT,
    "AuthorProfileURL"  TEXT,
    "Author"    TEXT,
    "Title" TEXT,
    "OriginalSize"  INTEGER,
    "OriginalMD5"   TEXT,
    "Thumbnail300KURL"  TEXT,
    "Rotation"  INTEGER,
    "filename"  TEXT,
    "package_name"  TEXT, "package_cid" TEXT, "latitude" TEXT, "longitude" TEXT, "altitude" TEXT, "created" TEXT,
    PRIMARY KEY("ImageID")
);
CREATE TABLE IF NOT EXISTS 'workflow_status' ('id' INTEGER, 'image_id' TEXT, 'task' TEXT, 'status' TEXT, 'timestamp' TEXT, FOREIGN KEY ('image_id') REFERENCES 'open_images'('ImageID'), PRIMARY KEY('id'));
CREATE INDEX images_status ON workflow_status ('status');
CREATE INDEX image_status ON workflow_status ('image_id');