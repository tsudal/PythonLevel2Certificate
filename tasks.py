from robocorp.tasks import task
from resources.process import *


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    
    PS. I took some liberties with changing some libraries to more pytonic ones,
    because rules don't say that I have to use RPAframework stuff, so:
    - RPA.HTTP got replaced with requests to download csv.
    - RPA.Tables got replaced with csv, i just like output of that better than pandas-like output from Tables.
    - RPA.Archive went bye bye and shutil took it place to create zip.
    I also added jinja2 to preserve image of receipt better.
    RPA.PDF is fine, and if I would like to replace this with pypdf I would have to fight bunch of conflicting dependencies
    and I don't have time nor sugar needed to deal with that ;)
    """
    
    browser.configure(
        slowmo = 200
        )
    download_robot_orders()
    go_to_robot_order_website()
    
    for order in read_csv():
        print(order)
        close_annoying_modal(order['Order number'])
        fill_the_form(order=order)
        screenshot_robot(order['Order number'])
        store_receipt_as_pdf(order['Order number'])
        order_anoter_bot()

    archive_receipts()
    clean_up_after_process()
    