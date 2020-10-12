# EXPORT THE DATABASE AFTER RUNNING THIS SCRIPT AND IMPORT AS NEW DBASE TO
# DRASTICALLY REDUCE SIZE

import sqlite3
import os

images_db = "map/deplatformr_open_images_v6.sqlite"
db = sqlite3.connect(images_db)
cursor = db.cursor()

"""
print("Deleting non-geo images from database. This will take a while.")
cursor.execute = ("DELETE FROM open_images WHERE latitude IS NULL")
db.commit()

print("Creating annotations table.")
cursor.execute("CREATE TABLE "annotations" ("id" INTEGER, ImageID" TEXT, "DisplayName" TEXT, "Type" TEXT, "Function" TEXT, "Confidence" INTEGER, "XMin1" TEXT, "XMax1" TEXT, "YMin1" TEXT, "YMax1" TEXT, "RelationshipLabel" TEXT, "DisplayName2"  INTEGER, "XMin2" TEXT, "XMax2" TEXT, "YMin2" TEXT, "YMax2" TEXT, "isOccluded" TEXT, "isTruncated" TEXT, "isGroupOf" TEXT, "isDepiction" TEXT, "isInside" TEXT, "MaskPath" TEXT, "BoxID" TEXT, "PredictedIoU" TEXT, "Clicks" TEXT) PRIMARY KEY("id")")
db.commit()
"""

print("Populating image relationships in the annotations table.")
cursor.execute("SELECT ImageID FROM open_images")
images = cursor.fetchall()
for image in images:
    image_id = image[0]

    # Labels
    cursor.execute(
        "SELECT labels.DisplayName, train_labels_human.Confidence FROM labels INNER JOIN train_labels_human ON train_labels_human.LabelName = labels.LabelName WHERE train_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence) VALUES (?,?,?,?,?)",
                           (image_id, result[0], "tag", "training", result[1],))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, test_labels_human.Confidence FROM labels INNER JOIN test_labels_human ON test_labels_human.LabelName = labels.LabelName WHERE test_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence) VALUES (?,?,?,?,?)",
                           (image_id, result[0], "tag", "testing", result[1],))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, validate_labels_human.Confidence FROM labels INNER JOIN validate_labels_human ON validate_labels_human.LabelName = labels.LabelName WHERE validate_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence) VALUES (?,?,?,?,?)",
                           (image_id, result[0], "tag", "validation", result[1],))
        db.commit()

    # Boxes
    cursor.execute(
        "SELECT labels.DisplayName, train_boxes.Confidence, train_boxes.XMin, train_boxes.XMax, train_boxes.YMin, train_boxes.YMax, train_boxes.IsOccluded, train_boxes.IsTruncated, train_boxes.IsGroupOf, train_boxes.isDepiction, train_boxes.isInside FROM train_boxes INNER JOIN labels ON train_boxes.LabelName = labels.LabelName WHERE train_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence, XMin1, Xmax1, YMin1, YMax1, isOccluded, isTruncated, isGroupOf, isDepiction, isInside) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "box", "training", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, test_boxes.Confidence, test_boxes.XMin, test_boxes.XMax, test_boxes.YMin, test_boxes.YMax, test_boxes.IsOccluded, test_boxes.IsTruncated, test_boxes.IsGroupOf, test_boxes.isDepiction, test_boxes.isInside FROM test_boxes INNER JOIN labels ON test_boxes.LabelName = labels.LabelName WHERE test_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence, XMin1, Xmax1, YMin1, YMax1, isOccluded, isTruncated, isGroupOf, isDepiction, isInside) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "box", "testing", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, validate_boxes.Confidence, validate_boxes.XMin, validate_boxes.XMax, validate_boxes.YMin, validate_boxes.YMax, validate_boxes.IsOccluded, validate_boxes.IsTruncated, validate_boxes.IsGroupOf, validate_boxes.isDepiction, validate_boxes.isInside FROM validate_boxes INNER JOIN labels ON validate_boxes.LabelName = labels.LabelName WHERE validate_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, Confidence, XMin1, Xmax1, YMin1, YMax1, isOccluded, isTruncated, isGroupOf, isDepiction, isInside) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "box", "validation", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    # Relationships
    cursor.execute("SELECT l1.DisplayName, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM train_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, DisplayName2, RelationshipLabel, Type, Function, XMin1, Xmax1, YMin1, YMax1, XMin2, Xmax2, YMin2, YMax2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], result[1], result[2], "relationship", "training", result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    cursor.execute("SELECT l1.DisplayName, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM test_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, DisplayName2, RelationshipLabel, Type, Function, XMin1, Xmax1, YMin1, YMax1, XMin2, Xmax2, YMin2, YMax2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], result[1], result[2], "relationship", "testing", result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    cursor.execute("SELECT l1.DisplayName, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM validate_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, DisplayName2, RelationshipLabel, Type, Function, XMin1, Xmax1, YMin1, YMax1, XMin2, Xmax2, YMin2, YMax2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], result[1], result[2], "relationship", "validation", result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
        db.commit()

    # Segmentations

    cursor.execute(
        "SELECT labels.DisplayName, train_segmentations.MaskPath, train_segmentations.BoxID, train_segmentations.BoxXMin, train_segmentations.BoxXMax, train_segmentations.BoxYMin, train_segmentations.BoxYMax, train_segmentations.PredictedIoU, train_segmentations.Clicks FROM train_segmentations INNER JOIN labels ON train_segmentations.LabelName = labels.LabelName WHERE train_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, MaskPath, BoxID, XMin1, Xmax1, YMin1, YMax1, PredictedIoU, Clicks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "segmentation", "training", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, validate_segmentations.MaskPath, validate_segmentations.BoxID, validate_segmentations.BoxXMin, validate_segmentations.BoxXMax, validate_segmentations.BoxYMin, validate_segmentations.BoxYMax, validate_segmentations.PredictedIoU, validate_segmentations.Clicks FROM validate_segmentations INNER JOIN labels ON validate_segmentations.LabelName = labels.LabelName WHERE validate_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, MaskPath, BoxID, XMin1, Xmax1, YMin1, YMax1, PredictedIoU, Clicks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "segmentation", "validation", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]))
        db.commit()

    cursor.execute(
        "SELECT labels.DisplayName, test_segmentations.MaskPath, test_segmentations.BoxID, test_segmentations.BoxXMin, test_segmentations.BoxXMax, test_segmentations.BoxYMin, test_segmentations.BoxYMax, test_segmentations.PredictedIoU, test_segmentations.Clicks FROM test_segmentations INNER JOIN labels ON test_segmentations.LabelName = labels.LabelName WHERE test_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        for result in results:
            cursor.execute("INSERT INTO annotations (ImageID, DisplayName, Type, Function, MaskPath, BoxID, XMin1, Xmax1, YMin1, YMax1, PredictedIoU, Clicks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                           (image_id, result[0], "segmentation", "testing", result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]))
        db.commit()

db.close()
