from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import re
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

Window.size = (370, 600)


class Users(MDApp):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    database = mysql.connector.connect(host="localhost", user="root", password="wande2233", database="trendy")
    cursor = database.cursor()
    cursor.execute("select*from users")
    for i in cursor.fetchall():
        print(i[0], i[1])


class TrendyApp(MDApp):

    def show_custom_bottom_sheet(self, image, price, rate):
        bottom_sheet = Factory.ContentCustomSheet()
        bottom_sheet.rate = rate
        bottom_sheet.image = image
        bottom_sheet.price = price
        self.custom_sheet = MDCustomBottomSheet(screen=bottom_sheet)
        self.custom_sheet.open()

    def build(self):
        self.title = 'Trendy Foot Wear'
        self.theme_cls.primary_palette = "Orange"
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("home.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("shoes.kv"))
        screen_manager.add_widget(Builder.load_file("women.kv"))
        screen_manager.add_widget(Builder.load_file("kids.kv"))
        screen_manager.add_widget(Builder.load_file("billing.kv"))
        return screen_manager

    def send_data(self, email, password):

        if re.fullmatch(self.regex, email.text):
            self.cursor.execute(f"insert into login values('{email.text}','{password.text}')")
            self.database.commit()
            email.text = ""
            password.text = ""

    def receive_data(self, email, password):
        self.cursor.text("select * from login")
        email_list = []
        for i in self.cursor.fetchall():
            email_list.append(i[0])
        if email.text in email_list and email.text != "":
            self.cursor.execute(f"select password from login where email='{email.text}'")
            for j in self.cursor:
                if password.text == j[0]:
                    print("You have Successfully LoggedIn!")
                else:
                    print("Incorrect Password")
        else:
            print("Incorrect Email")


TrendyApp().run()
