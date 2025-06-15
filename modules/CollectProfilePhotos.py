"""
This module is needed for the training of the model, which divides the baddies from the juggernauts
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from modules.IAutomat import IAutomat
from PIL import Image
import sys
import os
import traceback

class CollectProfilePhotos(IAutomat):
    def __init__(self, phone, cropTop:tuple, cropBottom:tuple, iterations:int):
        super().__init__(phone)
        self.crop_box = None
        if len(cropBottom) == 2 and len(cropTop) == 2:
            self.crop_box = tuple(list(cropTop) + list(cropBottom))
        self.iterations = iterations
    
    def yieldPhotos(self):
        sleep(3)
        try_count = 0
        for i in range(self.iterations):
            try:
                if os.path.exists(f"{os.getcwd()}/pics/") == False:
                    os.mkdir("pics")
                lista = self.driver.find_elements(By.TAG_NAME,"button")
                if lista[-3].is_displayed() and lista[-3].text == "TETSZIK":
                    self.driver.save_screenshot(filename=f"{os.getcwd()}/pics/{i}.png")
                    image = Image.open(f"{os.getcwd()}/pics/{i}.png")
                    cropped_image = image.crop(self.crop_box)
                    cropped_image.save(f"{os.getcwd()}/pics/{i}.png")
                    lista[-3].click()
                else:
                    self.driver.get("https://tinder.com/")
                    continue
            except Exception as e:
                if os.path.exists(f"{os.getcwd()}/pics/{i}.png"):
                    os.remove(f"{os.getcwd()}/pics/{i}.png")
                print("Cannot find the needed button. Retrying...",file=sys.stderr)
                traceback.print_exc()
                self.driver.get("https://tinder.com/")
                if try_count == 3:
                    exit(1)
                try_count += 1
                sleep(3)
            sleep(0.5)