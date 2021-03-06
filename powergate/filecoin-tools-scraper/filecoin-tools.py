from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sqlite3

abs_path = os.getcwd()
split = os.path.split(abs_path)

workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")

workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()
cursor.execute("SELECT cid FROM packages WHERE cid IS NOT NULL")
# if run needs to be resumed for a specific date range of packages:
#cursor.execute("SELECT cid FROM packages WHERE cid IS NOT NULL AND timestamp > ?", ("2020-10-16 06:10:54.294597",),)
cids = cursor.fetchall()


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = os.path.join(abs_path, 'chromedriver')
driver = webdriver.Chrome(executable_path=DRIVER_PATH)  # open browser windows
# driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)  # headless

count = 0
total_deals = 0

for cid in cids:
    count += 1
    print("CID " + str(count) + " of " + str(len(cids)))
    print("Payload CID " + cid[0])
    try:
        filepath = "https://filecoin.tools/" + cid[0]
        driver.get(filepath)

        # Wait for page data to render
        time.sleep(15)

        deals = driver.find_elements_by_class_name('sc-fzoLag')
        piece_cid = driver.find_element_by_class_name('sc-fzoyTs').text
        print("Piece CID " + piece_cid)
    except Exception as e:
        print("No deals found")
        continue

    active_deals = 0

    for deal in deals:
        detail = deal.find_element_by_class_name("sc-fzoNJl").click()
        # Wait for modal pop-up
        time.sleep(3)
        driver.switch_to.active_element
        rows = driver.find_elements_by_class_name('row')
        for row in rows:
            try:
                label = row.find_element_by_class_name('fCkJVF').text
                value = row.find_element_by_class_name('gLiaon').text
                if label == "Deal ID":
                    deal_id = int(value)
                    continue
                if label == "Miner ID":
                    miner_id = value
                    continue
                if label == "Client":
                    client_id = value
                    continue
                if label == "Piece Size":
                    piece_size = int(value)
                    continue
                if label == "Start Deal":
                    start_epoch = int(value)
                    continue
                if label == "End Deal":
                    end_epoch = int(value)
                    continue
                if label == "Price":
                    price = int(value)
                    continue
                if label == "Status":
                    if value == "Active":
                        active_deals += 1
                        cursor.execute("INSERT INTO deals (deal_id, payload_cid, piece_cid, piece_size, miner_id, client_id, start_epoch, end_epoch, price) VALUES (?,?,?,?,?,?,?,?,?)", (
                            deal_id, cid[0], piece_cid, piece_size, miner_id, client_id, start_epoch, end_epoch, price),)
                        workflow_db.commit()

            except:
                continue

        driver.find_element_by_class_name("sc-fzoXWK.hnKkAN.is-center").click()
    print(str(active_deals) + " active deals")
    print("---------")
    total_deals += active_deals
    driver.switch_to.default_content

print("TOTAL ACTIVE DEALS: " + str(total_deals))
workflow_db.close()
driver.quit()
