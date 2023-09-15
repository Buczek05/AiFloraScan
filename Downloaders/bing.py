import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.FileHandler("bing_downloader.log"), logging.StreamHandler()],
)


import os, time, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from saving_photos import (
    FolderFilesManagement,
    SavingPhotoFromURLToFolderWithName,
)

FOLDER_PATH = os.path.join(os.getcwd(), "Images", "Bing")


class BingDownloader:
    def __init__(self, searching_term):
        self.searching_term = searching_term
        self.setup_folder_path()

    def setup_folder_path(self):
        self.folder_path = os.path.join(FOLDER_PATH, self.searching_term)
        self.create_folder_if_not_exists()

    def create_folder_if_not_exists(self):
        folders = self.folder_path.split("/")
        for i in range(1, len(folders)):
            folder = "/".join(folders[: i + 1])
            if not os.path.isdir(folder):
                os.mkdir(folder)

    def start_download(self):
        self.create_driver()
        self.open_bing()
        self.switch_to_img()
        self.accept_cookies()
        self.search_term()
        self.choose_fotografy_filter()
        self.load_all_photos()

    def create_driver(self):
        self.driver = webdriver.Chrome()

    def open_bing(self):
        self.driver.get("https://www.bing.com/")

    def switch_to_img(self):
        try:
            img_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[3]/div/div[3]/header/div[1]/nav/ul/li[2]/a",
                    )
                )
            )
            img_btn.click()
        except Exception as e:
            logging.error(e)
            raise Exception("Couldn't switch to images")

    def accept_cookies(self):
        try:
            coockies_btn = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div[2]/div[2]/button[1]",
                    )
                )
            )
            coockies_btn.click()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def search_term(self):
        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/header/form/div/input[1]")
                )
            )
            search_bar.send_keys("cat")
            search_bar.submit()
        except Exception as e:
            logging.error(e)
            raise Exception("Couldn't search term")

    def choose_fotografy_filter(self):
        self.click_filter_btn()
        self.click_type_btn()
        self.click_fotografy_choose_btn()

    def click_filter_btn(self):
        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/header/nav/span/span[2]/span/span")
            )
        ).click()

    def click_type_btn(self):
        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[4]/div[2]/div/ul/li[3]/span")
            )
        ).click()

    def click_fotografy_choose_btn(self):
        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[4]/div[2]/div/ul/li[3]/div/div/a[2]/span")
            )
        ).click()

    def load_all_photos(self):
        self.scroll_down()
        while True:
            try:
                self.click_button_and_scroll_down()
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

    def click_button_and_scroll_down(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div[5]/div[3]/div[3]/div[2]/a")
                )
            )
            button.click()
            self.scroll_down()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise Exception("Error - No button")

    def scroll_down(self):
        last_height = 0
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        while last_height != new_height:
            last_height = new_height
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            self.wait_until_scroll_height_changes_or_timeout(last_height, 5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

    def wait_until_scroll_height_changes_or_timeout(self, last_height, timeout):
        for i in range(timeout * 10):
            time.sleep(0.1)
            if (
                self.driver.execute_script("return document.body.scrollHeight")
                != last_height
            ):
                break

    def download_images(self):
        self.click_on_first_image()
        while True:
            pass

    def click_on_first_image(self):
        try:
            first_image = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div[5]/div[2]/ul/li[1]/div/div/a")
                )
            )
            first_image.click()
        except Exception as e:
            logging.error(e)
            raise Exception("Couldn't click on first image")

    def get_img(self):
        img = None
        try:
            img = self.get_single_image()
            print(img)
        except Exception as e:
            logging.error(e)
        if not img:
            try:
                imgs = self.get_multiple_image()
                print(imgs)
            except Exception as e:
                logging.error(e)
        

    def get_single_image(self):
        try:
            img = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div[1]/img",
                    )
                )
            )

            src = img.get_attribute("src")
            if src == None:
                src = img.get_attribute("data-src")
            return src
        except Exception as e:
            logging.error(e)
            return None

    def get_multiple_image(self):
        all_divs = self.driver.find_elements(By.CLASS_NAME, "slideViewCtnr")
        all_imgs = []
        for div in all_divs:
            img = self.get_single_imgage_from_div(div)
            all_imgs.append(img)
        return all_imgs

    def get_single_imgage_from_div(self, div: webdriver.Chrome._web_element_cls):
        img = div.find_element(By.TAG_NAME, "img")
        src = img.get_attribute("src")
        if src == None:
            src = img.get_attribute("data-src")
        return src


if __name__ == "__main__":
    bing = BingDownloader("cat")
    bing.start_download()
