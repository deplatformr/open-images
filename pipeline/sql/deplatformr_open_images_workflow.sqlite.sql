BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "packages" (
	"package_name"	TEXT,
	"package_cid"	TEXT,
	"cid_timestamp"	TEXT,
	PRIMARY KEY("package_name")
);
CREATE TABLE IF NOT EXISTS "images" (
	"image_id"	TEXT,
	"download"	INTEGER,
	"download_timestamp"	TEXT,
	"http_code"	TEXT,
	"filepath"	TEXT,
	"verify_checksum"	INTEGER,
	"verify_checksum_timestamp"	TEXT,
	"extract_metadata"	INTEGER,
	"extract_metadata_timestamp"	TEXT,
	"write_sidecar"	INTEGER,
	"write_sidecar_timestamp"	TEXT,
	"move_segmentations"	INTEGER,
	"move_segmentations_timestamp"	TEXT,
	"batch_size"	INTEGER,
	"batch_directory"	TEXT,
	"package_name"	TEXT,
	"package_timestamp"	TEXT
);
COMMIT;
