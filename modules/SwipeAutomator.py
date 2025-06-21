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
from modules.MailSender import MailSender
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from dotenv import load_dotenv
import os

mail = MailSender(os.getenv("FROM"),os.getenv("TO"))

class SwipeAutomator(IAutomat):
    def __init__(self,phone,filename,startDate=18,endDate=22,cropTop = None, cropBottom = None):
        super().__init__(phone)
        self.InEnd = endDate
        self.InStart = startDate
        self.startDate = self._setStart()
        self.endDate = self._setEnd()
        self.cropBox = tuple(list(cropTop) + list(cropBottom)) if cropTop != None and cropBottom != None else None
        self.filename = filename
        self._SendInfoTimes()
        
    def _setEnd(self):
        end = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,self.InEnd,0,0)
        return end if self.InEnd > self.startDate.hour else end + datetime.timedelta(days=1.0)
    
    def _setStart(self):
        return datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,self.InStart,0,0)
    
    def _SwipeRight(self,lista,isRight=True):
        num = -3 if isRight else -5
        displayed = lista[num].text in ["NEM","TETSZIK","NOPE","LIKE"]
        if lista[num].is_displayed() and displayed:
            lista[num].click()
        else:
            raise Exception("Element not found!")
        
    def _SendInfoTimes(self):
        info = f"""
                Dear User,
                Start of automated swiping scheduled at {self.startDate.year}-{self.startDate.month}-{self.startDate.day}: {self.startDate.hour}:{self.startDate.minute}:{self.startDate.second} {datetime.datetime.now().tzinfo.tzname()}.
                End of automated swiping scheduled at {self.endDate.year}-{self.endDate.month}-{self.endDate.day}: {self.endDate.hour}:{self.endDate.minute}:{self.endDate.second} {datetime.datetime.now().tzinfo.tzname()}
                """
        mail.SendMail("Notification: Swiping scheduled","Notification",info)
    
    def _IgnoreSuperLikes(self):
        isGood = True
        try:
            sleep(0.5)
            if len(self.driver.find_elements(By.TAG_NAME,"button")) != 0:
                texts = self.driver.find_elements(By.TAG_NAME,"button")[-1].text
                if texts in ["Köszönöm, nem", "No, thanks","Bezár","Close"]:
                    self.driver.find_elements(By.TAG_NAME,"button")[-1].click()
                    sleep(3)
                else:
                    raise Exception("Element not found!")
        except Exception:
            traceback.print_exc()
            sleep(3)
            self.driver.get("https://tinder.com/")
            isGood = False
        return isGood
    
    def _ErrorMessage(self,message):
        print(message,file=sys.stderr)
        mail.SendMail(f"Error: {message}","Error",message=f"{message} \n Please check the running agent! \n Tenderbot \n")
        exit(-1)
    
    def _ExecuteSwipes(self,model,cnn):
        lista = self.driver.find_elements(By.TAG_NAME,"button")
                    
        if cnn:
            image = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(image))
            cropped_image = image.crop(self.cropBox)
            resized_image = cropped_image.resize((224, 224))
            img_array = img_to_array(resized_image )
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            prediction = model.predict(img_array)
            self._SwipeRight(lista) if prediction[0][0] > 0.8 else self._SwipeRight(lista,False)
            print(f"Prediction for hotness: {prediction[0][0]:.2f}")
        else:
            self._SwipeRight(lista)
            
    def SwipeCNN(self, cnn=True):
        sleep(3)
        if cnn == True:
            if (os.path.exists(self.filename)):
                model = load_model(self.filename)
            else:
                self._ErrorMessage("The given file does not exists!")
        try_count = 0
        opened = True
        while True:
            if self.startDate.day != datetime.datetime.now().day:
                self.startDate = self._setStart()
                self.endDate = self._setEnd()
                self._SendInfoTimes()
            while self.startDate <= datetime.datetime.now() and datetime.datetime.now() <= self.endDate:
                print(f"Swiped at {datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}: {datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}")
                if opened == False:
                    self.driver = self.login.LoginWithProfile()
                    opened = True
                try:
                    self._ExecuteSwipes(model,cnn)
                except Exception as e:
                    mail.SendMail(f"Warning: Exception happened!","Warning",message=f"Exception happened!")
                    if self._IgnoreSuperLikes():
                        continue
                    print("Cannot find the needed button. Retrying...",file=sys.stderr)
                    traceback.print_exc()
                    if try_count == 3:
                        self.driver.close()
                        opened = False
                        try_count = 0
                        sleep(1796.5)
                    else:
                        try_count += 1
                        sleep(30)
                    sleep(3)
                sleep(0.5)
            if opened == True:
                self.driver.close()
                mail.SendMail(f"Notification: Tinder closed","Notification",message=f"Tinder closed.")
                opened = False
            sleep(2)