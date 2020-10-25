BEGIN TRANSACTION;
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
	"package_name"	TEXT,
	FOREIGN KEY("package_name") REFERENCES "packages_old"("name")
);
CREATE TABLE IF NOT EXISTS "packages" (
	"name"	TEXT,
	"timestamp"	TEXT,
	"size"	INTEGER,
	"cid"	TEXT,
	"cid_timestamp"	TEXT,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "jobs" (
	"job_id"	TEXT,
	"cid"	TEXT,
	"timestamp"	TEXT,
	"status"	TEXT,
	"ffs"	TEXT,
	FOREIGN KEY("cid") REFERENCES "packages"("cid"),
	PRIMARY KEY("job_id")
);
CREATE TABLE IF NOT EXISTS "deals" (
	"deal_id"	INTEGER,
	"payload_cid"	TEXT,
	"piece_cid"	TEXT,
	"piece_size"	INTEGER,
	"miner_id"	TEXT,
	"client_id"	TEXT,
	"start_epoch"	INTEGER,
	"end_epoch"	INTEGER,
	"price"	INTEGER,
	PRIMARY KEY("deal_id")
);
COMMIT;
