from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen  
import json, glob
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Nombre de usuario o contraseña incorrecta. Prueba de nuevo"
        

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
       with open("users.json") as file:
           users = json.load(file)
           
           
           users[uname] = {'username': uname, 'password': pword,
                           'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
           print(users)
           
           with open("users.json", 'w') as file:
               json.dump(users, file)
           self.manager.current = "sign_up_screen_success"
               

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        
        self.manager.transition.direction = 'right' # or 'left'
        self.manager.current = "login_screen" 
        
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right' 
        self.manager.current = "login_screen" #return to login screen

    def get_quote(self, feel):
        feel= feel.lower()
        available_recipes = glob.glob("quotes/*txt")
        
        
        available_recipes = [Path(filename).stem for filename in available_recipes]
        
        if feel in available_recipes:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes) # use ramdom.choice to get a random quote
        else:
            self.ids.quote.text = "Prueba con: hamburguesas, ensaladas, cocktails, batidos..."
            
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass
class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == '__main__':
    MainApp().run()