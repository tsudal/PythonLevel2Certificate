from robocorp import log,browser
from RPA.PDF import PDF
from csv import DictReader
from jinja2 import Environment, BaseLoader
import requests
import os
import time as clock
import shutil

def download_robot_orders() -> None:
    """
    Using request library download orders.csv and save it in orderdocs folder.
    """
    try:
        get_csv = requests.get("https://robotsparebinindustries.com/orders.csv", allow_redirects=True)
        open("output//orders.csv", "wb").write(get_csv.content)
        
    except requests.exceptions.RequestException as d_err:
        log.exception(f"{type(d_err).__name__}: {d_err}")
        raise d_err
    
def read_csv() -> dict:
    """
    Using CSV library convert csv into list of dictionaries(rows) and remove order.csv file
    """
    try:
        with open("output//orders.csv", "r") as convert_csv:
            new_dict = DictReader(convert_csv)
            robot_orders = list(new_dict)
    
        os.remove("output//orders.csv")
        return robot_orders
    
    except (FileNotFoundError, FileExistsError) as f_err:
        log.exception(f"{type(f_err).__name__}: {f_err}")
        raise f_err
    
def go_to_robot_order_website() -> None:
    """
    Configure browser and load initial page
    """

    try:
        browser.goto("https://robotsparebinindustries.com/#/robot-order")
        page = browser.page()
    
    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err
    
def close_annoying_modal(order_number) -> None:
    """
    Function to close pop up about selling my soul or something ;P
    """
    try:
        clock.sleep(1)
        page = browser.page()
        order_no = order_number
        check_if_still_showing = page.get_by_role("button", name="I guess so...").is_visible()
        while check_if_still_showing == True:
            if order_no== "1" or order_no =="2":
                page.get_by_role("button", name="OK").click()
            elif order_no == "3" or order_no =="4":
                page.get_by_role("button", name="Yep").click()
            else:
                page.get_by_role("button", name="I guess so...").click()
            clock.sleep(1)   
            check_if_still_showing = page.get_by_role("button", name="I guess so...").is_visible()


        
    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err

def fill_the_form(order :dict) -> None:
    """
    Place robot order for each element in the list.
    """
    try:
        page = browser.page()
        page.locator("#head").select_option(order['Head'])
        page.locator(f"#id-body-{order['Body']}").click()
        page.get_by_placeholder("Enter the part number for the").fill(order["Legs"])
        page.get_by_placeholder("Shipping address").fill(order["Address"])
        page.get_by_role("button", name="Preview").click()
        page.get_by_role("button", name="ORDER").click()
        clock.sleep(1)
        check_receipt = page.locator('#receipt').is_visible(timeout=10.0)
        print(check_receipt)
        while check_receipt != True:
            page = browser.page()
            page.get_by_role("button", name="ORDER").click()
            check_receipt = page.locator('#receipt').is_visible(timeout=10.0)

    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err

def order_anoter_bot() -> None:
    """
    Click order another robot button
    """
    try:
        page = browser.page()
        page.locator("#order-another").click()
        
        
    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err

def store_receipt_as_pdf(order_number) -> None:
    """
    Create receipt pdf for each order
    """
    try:
        page = browser.page()
        header = page.get_by_role('heading',level=1).inner_html()
        receipt_img1 = f"output//screenshots//receipt{order_number}.png"
        receipt_img2 = f"output//screenshots//robot{order_number}.png"
        receipt = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="style.css" />
        </head>
        <body>
        <h1 align="center">{{ header }}</h1>
        <table>
            <tr>
            <td><img src={{ img1 }}></td>
            <td><img src={{ img2 }}></td>
            </tr>
        </table>
        </body>
        </html>
        """
        env_jin = Environment(loader=BaseLoader())
        receipt_template = env_jin.from_string(receipt)
        content = receipt_template.render({"header":f"{header}", "img1": f"{receipt_img1}", "img2": f"{receipt_img2}"})
        new_pdf = PDF()
        new_pdf.html_to_pdf(content, f"output//receipts//{order_number}.pdf")

            
    except (FileNotFoundError, FileExistsError) as f_err:
        log.exception(f"{type(f_err).__name__}: {f_err}")
        raise f_err
    
    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err
    
def screenshot_robot(order_number) -> None:
    """
    Take screenshot of receipt and robot preview for pdf receipt document
    """
    try:
        clock.sleep(1)
        page = browser.page()
        receipt_path = f"output//screenshots//receipt{order_number}.png"
        robot_preview_path = f"output//screenshots//robot{order_number}.png"
        page.locator('#receipt').screenshot(path=receipt_path)
        page.locator("#robot-preview-image").screenshot(path=robot_preview_path)
        
    except TimeoutError as t_err:
        log.exception(f"{type(t_err).__name__}: {t_err}")
        raise t_err

    except browser.BrowserNotFound as b_err:
        log.exception(f"{type(b_err).__name__}: {b_err}")
        raise b_err
    
def archive_receipts() -> None:
    """
    Create zip archive of all generated receipts
    """
    try:
        shutil.make_archive("output//receipts", "zip", "output//", "receipts")
            
        
    except (FileNotFoundError, FileExistsError) as f_err:
        log.exception(f"{type(f_err).__name__}: {f_err}")
        raise f_err
    
def clean_up_after_process() -> None:
    """
    Remove screenshots and receipt folders with data left after the process
    """
    try:
        shutil.rmtree("output//receipts")
        shutil.rmtree("output//screenshots")
    
    except (FileNotFoundError, FileExistsError) as f_err:
        log.exception(f"{type(f_err).__name__}: {f_err}")
        raise f_err