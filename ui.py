from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color
import time
from kivy.core.window import Window
import os
from functools import partial
from kivy.uix.textinput import TextInput


class MainScreen(Screen):
    def __init__(self,sm,**kwargs):
        super (MainScreen,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical' , size_hint = (0.5,0.08) , pos=(200,450))
        textinput = TextInput(text='Hello world' , multiline=False)

        fc = FileChooserListView()
    	
    	box_parent.add_widget(textinput)
    	self.add_widget(fc)

class TestApp(App):
    def build(self):
        Window.size = (800, 500)

        sm = ScreenManager()
        
        main_screen = MainScreen(sm , name='main_screen')
        sm.add_widget(main_screen)

        return sm


if __name__=="__main__":
    TestApp().run()

