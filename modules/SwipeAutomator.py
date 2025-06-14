"""
Where you find the holly molly.
"""

import io
from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image
import os
import sys
import traceback
import datetime
import numpy as np
from modules.IAutomat import IAutomat
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class SwipeAutomator(IAutomat):
    def __init__(self,phone,filename,startDate=18,endDate=22):
        super().__init__(phone)
        end = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,endDate,0,0)
        self.startDate = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,startDate,0,0)
        self.endDate = end if endDate > datetime.datetime.now().hour else end + datetime.timedelta(days=1.0)
        self.filename = filename
    
    def _SwipeRight(self,lista,isRight=True):
        num = -3 if isRight else -5
        displayed = lista[-5].text == "NEM" or lista[-3].text == "TETSZIK" or lista[-5].text == "NOPE" or lista[-3].text == "LIKE"
        if lista[num].is_displayed() and displayed:
            lista[num].click()
        else:
            raise Exception("Element not found!")
    
    def _IgnoreSuperLikes(self):
        isGood = True
        try:
            if len(self.driver.find_elements(By.TAG_NAME,"button")) != 0:
                texts = self.driver.find_elements(By.TAG_NAME,"button")[-1].text
                if texts == "Köszönöm, nem" or texts == "No, thanks":
                    self.driver.find_elements(By.TAG_NAME,"button")[-1].click()
                else:
                    raise Exception
            else:
                raise Exception
        except Exception:
            traceback.print_exc()
            self.driver.get("https://tinder.com/")
            isGood = False
        return isGood
    
    def _ErrorMessage(self,message):
        print(message,file=sys.stderr)
        exit(-1)
            
    def SwipeCNN(self, cnn=True):
        sleep(3)
        if cnn == True:
            if self.filename == None:
                self._ErrorMessage("Before you dive in, please generate the model or turn off the AI switch!")
            else:
                if (os.path.exists(self.filename)):
                    model = load_model(self.filename)
                else:
                    self._ErrorMessage("The given file does not exists!")
        try_count = 0
        opened = True
        while True:
            while self.startDate <= datetime.datetime.now() and datetime.datetime.now() <= self.endDate:
                if opened == False:
                    self.driver = self.login.LoginWithProfile()
                    opened = True
                try:
                    lista = self.driver.find_elements(By.TAG_NAME,"button")
                
                    if cnn:
                        image = self.driver.get_screenshot_as_png()
                        image = Image.open(io.BytesIO(image))
                        crop_box = (1616, 90, 2162, 1034)
                        cropped_image = image.crop(crop_box)
                        resized_image = cropped_image.resize((224, 224))
                        img_array = img_to_array(resized_image )
                        img_array = img_array / 255.0
                        img_array = np.expand_dims(img_array, axis=0)
                        prediction = model.predict(img_array)
                        self._SwipeRight(lista) if prediction[0][0] > 0.8 else self._SwipeRight(lista,False)
                        print(f"Prediction for hotness: {prediction[0][0]:.2f}")
                    else:
                        self._SwipeRight(lista)
                except Exception as e:
                    if self._IgnoreSuperLikes():
                        continue
                    print("Cannot find the needed button. Retrying...",file=sys.stderr)
                    traceback.print_exc()
                    if try_count == 3:
                        exit(1)
                    try_count += 1
                    sleep(3)
                sleep(0.5)
            if opened == True:
                self.driver.close()
                opened = False
            sleep(2)