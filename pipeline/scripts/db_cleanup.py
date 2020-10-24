import sqlite3
import os


db_path = os.path.join(os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)

cursor = workflow_db.cursor()
cursor.execute("SELECT image_id from images WHERE package_name = ?", (
    "deplatformr-open-images-3.tar",),)
results = cursor.fetchall()
cursor.close()
print("found " + str(len(results)) + " results.")

cursor = images_db.cursor()
for result in results:
    print(result[0])
    cursor.execute("UPDATE open_images set package_name = ? where image_id = ?",
                   ("deplatformr-open-images-3.tar", result[0],),)
workflow_db.commit()
workflow_db.close()
