import sqlite3
import os

db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)
cursor = images_db.cursor()

def retrieve_annotations(image_id):

    annotations = {}

    # Labels
    cursor.execute(
        "SELECT labels.LabelName, labels.DisplayName FROM labels INNER JOIN train_labels_human ON train_labels_human.LabelName = labels.LabelName WHERE train_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        labels = {}
        for result in results:
            labels[result[0]] = result[1]
        annotations["trainingLabels"] = labels

    cursor.execute(
        "SELECT labels.LabelName, labels.DisplayName FROM labels INNER JOIN validate_labels_human ON validate_labels_human.LabelName = labels.LabelName WHERE validate_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        labels = {}
        for result in results:
            labels[result[0]] = result[1]
        annotations["validationLabels"] = labels

    cursor.execute(
        "SELECT labels.LabelName, labels.DisplayName FROM labels INNER JOIN test_labels_human ON test_labels_human.LabelName = labels.LabelName WHERE test_labels_human.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        labels = {}
        for result in results:
            labels[result[0]] = result[1]
        annotations["testingLabels"] = labels

    # Boxes
    cursor.execute(
        "SELECT train_boxes.LabelName, labels.DisplayName, train_boxes.Confidence, train_boxes.XMin, train_boxes.XMax, train_boxes.YMin, train_boxes.YMax, train_boxes.IsOccluded, train_boxes.IsTruncated, train_boxes.IsGroupOf, train_boxes.isDepiction, train_boxes.isInside FROM train_boxes INNER JOIN labels ON train_boxes.LabelName = labels.LabelName WHERE train_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        boxes = []
        for result in results:
            boxes.append({result[0]: result[1], "confidence": result[2], "xMin": result[3], "xMax": result[4], "yMin": result[5], "yMax": result[6],
                          "isOccluded": result[7], "isTruncated": result[8], "isGroupOf": result[9], "isDepiction": result[10], "isInside": result[11]})
        annotations["trainingBoxes"] = boxes

    cursor.execute(
        "SELECT validate_boxes.LabelName, labels.DisplayName, validate_boxes.Confidence, validate_boxes.XMin, validate_boxes.XMax, validate_boxes.YMin, validate_boxes.YMax, validate_boxes.IsOccluded, validate_boxes.IsTruncated, validate_boxes.IsGroupOf, validate_boxes.isDepiction, validate_boxes.isInside FROM validate_boxes INNER JOIN labels ON validate_boxes.LabelName = labels.LabelName WHERE validate_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        boxes = []
        for result in results:
            boxes.append({result[0]: result[1], "confidence": result[2], "xMin": result[3], "xMax": result[4], "yMin": result[5], "yMax": result[6],
                          "isOccluded": result[7], "isTruncated": result[8], "isGroupOf": result[9], "isDepiction": result[10], "isInside": result[11]})
        annotations["validationBoxes"] = boxes

    cursor.execute(
        "SELECT test_boxes.LabelName, labels.DisplayName, test_boxes.Confidence, test_boxes.XMin, test_boxes.XMax, test_boxes.YMin, test_boxes.YMax, test_boxes.IsOccluded, test_boxes.IsTruncated, test_boxes.IsGroupOf, test_boxes.isDepiction, test_boxes.isInside FROM test_boxes INNER JOIN labels ON test_boxes.LabelName = labels.LabelName WHERE test_boxes.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        boxes = []
        for result in results:
            boxes.append({result[0]: result[1], "confidence": result[2], "xMin": result[3], "xMax": result[4], "yMin": result[5], "yMax": result[6],
                          "isOccluded": result[7], "isTruncated": result[8], "isGroupOf": result[9], "isDepiction": result[10], "isInside": result[11]})
        annotations["testingBoxes"] = boxes

    # Relationships
    cursor.execute("SELECT r.LabelName1, l1.DisplayName, r.LabelName2, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM train_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        relationships = []
        for result in results:
            relationships.append(
                {"relationship": result[1] + " " + result[4] + " " + result[3], "relationshipLabel": result[4], "box1": {result[0]: result[1], "xMin": result[5], "xMax": result[6], "yMin": result[7], "yMax": result[8]}, "box2": {result[2]: result[3], "xMin": result[9], "xMax": result[10], "yMin": result[11], "yMax": result[12]}})
        annotations["trainingRelationships"] = relationships

    cursor.execute("SELECT r.LabelName1, l1.DisplayName, r.LabelName2, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM validate_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        relationships = []
        for result in results:
            relationships.append(
                {"relationship": result[1] + " " + result[4] + " " + result[3], "relationshipLabel": result[4], "box1": {result[0]: result[1], "xMin": result[5], "xMax": result[6], "yMin": result[7], "yMax": result[8]}, "box2": {result[2]: result[3], "xMin": result[9], "xMax": result[10], "yMin": result[11], "yMax": result[12]}})
        annotations["validationRelationships"] = relationships

    cursor.execute("SELECT r.LabelName1, l1.DisplayName, r.LabelName2, l2.DisplayName, r.RelationshipLabel, r.Xmin1, r.XMax1, r.YMin1, r.YMax1, r.XMin2, r.XMax2, r.YMin2, r.YMax2 FROM test_relationships r LEFT JOIN labels l1 ON r.LabelName1 = l1.LabelName LEFT JOIN labels l2 ON r.LabelName2 = l2.LabelName WHERE r.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        relationships = []
        for result in results:
            relationships.append(
                {"relationship": result[1] + " " + result[4] + " " + result[3], "relationshipLabel": result[4], "box1": {result[0]: result[1], "xMin": result[5], "xMax": result[6], "yMin": result[7], "yMax": result[8]}, "box2": {result[2]: result[3], "xMin": result[9], "xMax": result[10], "yMin": result[11], "yMax": result[12]}})
        annotations["testingRelationships"] = relationships

    # Segmentations

    cursor.execute(
        "SELECT train_segmentations.LabelName, labels.DisplayName, train_segmentations.MaskPath, train_segmentations.BoxID, train_segmentations.BoxXMin, train_segmentations.BoxXMax, train_segmentations.BoxYMin, train_segmentations.BoxYMax, train_segmentations.PredictedIoU, train_segmentations.Clicks FROM train_segmentations INNER JOIN labels ON train_segmentations.LabelName = labels.LabelName WHERE train_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        segmentations = []
        for result in results:
            segmentations.append({result[0]: result[1], "maskFile": result[2], "boxId": result[3], "xMin": result[4],
                                  "xMax": result[5], "yMin": result[6], "yMax": result[7], "PredictedIoU": result[8], "clicks": result[9]})
        annotations["trainingSegmentations"] = segmentations

    cursor.execute(
        "SELECT validate_segmentations.LabelName, labels.DisplayName, validate_segmentations.MaskPath, validate_segmentations.BoxID, validate_segmentations.BoxXMin, validate_segmentations.BoxXMax, validate_segmentations.BoxYMin, validate_segmentations.BoxYMax, validate_segmentations.PredictedIoU, validate_segmentations.Clicks FROM validate_segmentations INNER JOIN labels ON validate_segmentations.LabelName = labels.LabelName WHERE validate_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        segmentations = []
        for result in results:
            segmentations.append({result[0]: result[1], "maskFile": result[2], "boxId": result[3], "xMin": result[4],
                                  "xMax": result[5], "yMin": result[6], "yMax": result[7], "PredictedIoU": result[8], "clicks": result[9]})
        annotations["validationSegmentations"] = segmentations

    cursor.execute(
        "SELECT test_segmentations.LabelName, labels.DisplayName, test_segmentations.MaskPath, test_segmentations.BoxID, test_segmentations.BoxXMin, test_segmentations.BoxXMax, test_segmentations.BoxYMin, test_segmentations.BoxYMax, test_segmentations.PredictedIoU, test_segmentations.Clicks FROM test_segmentations INNER JOIN labels ON test_segmentations.LabelName = labels.LabelName WHERE test_segmentations.ImageID = ?", (image_id,),)
    results = cursor.fetchall()
    if len(results) > 0:
        segmentations = []
        for result in results:
            segmentations.append({result[0]: result[1], "maskFile": result[2], "boxId": result[3], "xMin": result[4],
                                  "xMax": result[5], "yMin": result[6], "yMax": result[7], "PredictedIoU": result[8], "clicks": result[9]})
        annotations["testingSegmentations"] = segmentations

    return(annotations)
