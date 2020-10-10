import sqlite3


db_path = os.path.join(os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)

cursor = images_db.cursor()
cursor.execute("SELECT ImageID from open_images WHERE package_name = ?"(
    "deplatformr-open-images4.tar",),)
results = cursor.fetchall()
cursor.close()

cursor = workflow_db.cursor()
for result in results:
    cursor.execute("UPDATE images set package_name = ? where image_id = ?",
                   ("deplatformr-open-images-4.tar", result[0],),)
db.commit()
db.close()
