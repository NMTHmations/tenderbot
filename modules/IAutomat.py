from modules.LoginAgent import LoginAgent
import os

class IAutomat:
    def __init__(self,phone):
        self.phoneNumber = phone
        self.login = LoginAgent(self.phoneNumber)
        self.driver = self.login.LoginWithProfile() if os.path.exists("profile") else self.login.AutomatedLogin()