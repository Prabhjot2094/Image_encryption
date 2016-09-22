from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
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
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
class MainScreen(Screen):
    def __init__(self,sm,**kwargs):
        super (MainScreen,self).__init__(**kwargs)

        box_outermost = BoxLayout(orientation = 'vertical')
        relative_1 = BoxLayout(orientation = 'vertical' , size_hint = (1,1) , padding=(270,200,0,-50))
        
        btn_file_name = Button(text='Select Image' , pos=(200,-10) , size_hint=(0.5,0.01))

        box_1 = BoxLayout(orientation='horizontal',size_hint=(1,0.5),padding=(50,0))
        toggle_list = [0,0,0]
        checkbox_1 = Button(text="DES" ,size_hint=(1,0.4))
        checkbox_2 = Button(text="AES",size_hint=(1,0.4))
        checkbox_3 = Button(text="RSA",size_hint=(1,0.4))
       
        Box_2 = BoxLayout(orientation='horizontal',size_hint=(1,0.5))
        box_2 = RelativeLayout(orientation='horizontal',size_hint=(1,0.15))

        box_3 = BoxLayout(orientation='horizontal' , padding=(10,10))
        float_1 = BoxLayout()
        float_2 = FloatLayout()
        float_3 = BoxLayout()
        
        src_img = Image(id = 'src_img' , source = 'file_image1.png',size_hint=(1,1))
        dest_img = Image(id = 'dest_img' , source = 'test1.png',size=(1,1))
        btn_enc = Button(text="Encrypt" , pos=(330,20) , size_hint=(0.6,0.2))
        btn_dec = Button(text="Decrypt" , pos=(330,110) , size_hint=(0.6,0.2))
    
        #box_4 = BoxLayout(size_hint=(1,0.2))
        #btn_dummy = Button()
#------------------------------------Binding Widgets-------------------------------------------------------

        btn_file_name.bind(on_press=self.onClick)

        checkbox_1.bind(on_press=partial(self.EncSelect,toggle_list,0,checkbox_1,box_2))
        checkbox_2.bind(on_press=partial(self.EncSelect,toggle_list,1,checkbox_2,box_2))
        checkbox_3.bind(on_press=partial(self.EncSelect,toggle_list,2,checkbox_3,box_2))

#-------------------------------------Widgets are added----------------------------------------------------
    	
    	relative_1.add_widget(btn_file_name)
        
        box_1.add_widget(checkbox_1)
        box_1.add_widget(checkbox_3)
        box_1.add_widget(checkbox_2)

        float_1.add_widget(src_img)
        float_2.add_widget(btn_enc)
        float_2.add_widget(btn_dec)
        float_3.add_widget(dest_img)

        #box_2.add_widget(btn_dummy)
        box_3.add_widget(float_1)
        box_3.add_widget(float_2)
        box_3.add_widget(float_3)
        
        #box_4.add_widget(btn_dummy)

        box_outermost.add_widget(relative_1)
        box_outermost.add_widget(box_1)
        box_outermost.add_widget(box_2)
        #box_outermost.add_widget(box_4)
        box_outermost.add_widget(box_3)

    	self.add_widget(box_outermost)

#-------------------------------------Responsive Functions-------------------------------------------------

    def EncSelect(self,*args):
        btn_no = args[1]
        btn_pos = [54,521,287]
        enc_type = ['Enter key for DES Encryption','Enter key for AES Encryption']
        args[0][btn_no]=(args[0][btn_no]+1)%2
        
        if args[0][btn_no]==1:
            args[2].background_color=(0,0.2,0.8,1)
            if btn_no==2:
                return
            text_input = TextInput(id=str(btn_no),hint_text=enc_type[btn_no] , pos = (btn_pos[btn_no],0) , size_hint=(0.284,1))
            args[3].add_widget(text_input)
        else:    
            args[2].background_color=(0,0,0,1)
            if btn_no==2:
                return
            children = args[3].children
            for c in children:
                if c.id==str(btn_no):
                    args[3].remove_widget(c)
        
        print args[0]

    def onClick(self,*args):
        popup = Popup(title="Load file",size_hint=(0.9, 0.9))
        fc = FileChooserIconView() 
        popup.add_widget(fc)
        popup.open()
        fc.bind(on_submit=partial(self.onSubmit,fc,popup))
    def onSubmit(self,*args):
        file_name = (args[0].selection[0]).encode('utf-8')
        args[1].dismiss()
        
        src_img = Image(id = 'src_img' , source = file_name , size_hint=(1,1))
        self.children[0].children[0].add_widget(src_img)

            


class TestApp(App):
    def build(self):
        Window.size = (800, 500)
        Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()
        
        main_screen = MainScreen(sm , name='main_screen')
        sm.add_widget(main_screen)

        return sm


if __name__=="__main__":
    TestApp().run()

