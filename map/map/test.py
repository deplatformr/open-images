import sqlite3

images_db = "deplatformr-open-images.sqlite"
db = sqlite3.connect(images_db)
cursor = db.cursor()

cursor.execute("SELECT * FROM annotations")
annotations = cursor.fetchall()
tags = []
boxes = []
relationships = []
segmentations = []
for annotation in annotations:
    if annotation[3] == "tag":
        tags += [[annotation[4], annotation[5], annotation[2]]]
    if annotation[3] == "relationship":
        relationships += [[annotation[4], annotation[2], annotation[10], annotation[11], annotation[6], annotation[7],
                           annotation[8], annotation[9], annotation[12], annotation[13], annotation[14], annotation[15]]]
    if annotation[3] == "box":
        boxes += [[annotation[4], annotation[2], annotation[6], annotation[7],
                   annotation[8], annotation[9], annotation[16], annotation[17], annotation[18], annotation[19], annotation[20]]]
    if annotation[3] == "segmentation":
        segmentations += [[annotation[4], annotation[2], annotation[6], annotation[7],
                           annotation[8], annotation[9], annotation[21], annotation[23]]]

training_relationships = [
    relationship for relationship in relationships if relationship[0] == "training"]
validation_relationships = [
    relationship for relationship in relationships if relationship[0] == "validation"]
testing_relationships = [
    relationship for relationship in relationships if relationship[0] == "testing"]

training_boxes = [
    box for box in boxes if box[0] == "training"]
validation_boxes = [
    box for box in boxes if box[0] == "validation"]
testing_boxes = [
    box for box in boxes if box[0] == "testing"]

training_tags = [tag for tag in tags if tag[0] == "training"]
confident_training_tags = [tag for tag in training_tags if tag[1] == 1]
not_confident_training_tags = [tag for tag in training_tags if tag[1] == 0]

validation_tags = [tag for tag in tags if tag[0] == "validation"]
confident_validation_tags = [tag for tag in validation_tags if tag[1] == 1]
not_confident_validation_tags = [tag for tag in validation_tags if tag[1] == 0]

testing_tags = [tag for tag in tags if tag[0] == "testing"]
confident_testing_tags = [tag for tag in testing_tags if tag[1] == 1]
not_confident_testing_tags = [tag for tag in testing_tags if tag[1] == 0]

training_segmentations = [
    segmentation for segmentation in segmentations if segmentation[0] == "training"]
validation_segmentations = [
    segmentation for segmentation in segmentations if segmentation[0] == "validation"]
testing_segmentations = [
    segmentation for segmentation in segmentations if segmentation[0] == "confident_testing_tags"]
