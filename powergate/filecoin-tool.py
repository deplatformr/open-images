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
cids = cursor.fetchall()

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = '/Users/peter/Development/open-images/powergate/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)  # open browser windows
# driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)  # headless

count = 0

for cid in cids:
    count += 1
    filepath = "https://filecoin.tools/" + cid[0]
    driver.get(filepath)

    # Wait for page data to render
    time.sleep(7)

    deals = driver.find_elements_by_class_name('sc-fzoLag')
    piece_cid = driver.find_element_by_class_name('sc-fzoyTs').text
    print("CID " + str(count) + " of " + str(len(cids)))
    print("Payload CID " + cid[0])
    print("Piece CID " + piece_cid)

    active_deals = 0

    for deal in deals:
        detail = deal.find_element_by_class_name("sc-fzoNJl").click()
        # Wait for modal pop-up
        time.sleep(1)
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

    driver.switch_to.default_content

workflow_db.close()
driver.quit()
