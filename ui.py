import subprocess
import sys
import warnings
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
import file_binary
import json

class MainScreen(Screen):
    def __init__(self,sm,**kwargs):
        super (MainScreen,self).__init__(**kwargs)

        self.popup_back = 'imgz/transparent2.png'
        
        box_outermost = BoxLayout(orientation = 'vertical')
        relative_1 = RelativeLayout(orientation = 'vertical' , size_hint = (1,1))# , padding=(270,150,0,0))
        
        btn_file_name = Button(text='Select Image' , pos=(200,0) , font_size = '17sp', size_hint=(0.5,0.2),background_color=(0,0.2,0.8,1))
        logo = Image(source='imgz/logo_1.png' , pos=(77,45) , size_hint=(0.8,0.8))
        btn_header_enc = Button(text='Ciphers' , pos=(50,-58) , font_size = '17sp', size_hint=(0.875,0.2),background_color=(0,0.2,0.8,4),disabled=True , disabled_color=(1,1,1,1))

        box_1 = BoxLayout(orientation='horizontal',size_hint=(1,0.5),padding=(50,0),spacing=(2))
        toggle_list = [0,0,0]
        checkbox_1 = Button(text="DES", font_size = '17sp',size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5),background_down='atlas://data/images/defaulttheme/button')
        checkbox_2 = Button(text="RSA", font_size = '17sp',size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5),background_down='atlas://data/images/defaulttheme/button')
        checkbox_3 = Button(text="AES", font_size = '17sp',size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5),background_down='atlas://data/images/defaulttheme/button')

       
        Box_2 = BoxLayout(orientation='horizontal',size_hint=(1,0.5))
        box_2 = RelativeLayout(orientation='horizontal',size_hint=(1,0.15))

        box_3 = BoxLayout(orientation='horizontal' , padding=(10,10))
        float_1 = BoxLayout()
        float_2 = FloatLayout()
        float_3 = BoxLayout()
        
        src_img = Image(id = 'src_img' , source = 'imgz/default.jpg',size_hint=(1,1))
        dest_img = Image(id = 'dest_img' , source = 'imgz/default.jpg',size=(1,1))
        btn_enc = Button(text="Encrypt" , pos=(330,50) , size_hint=(0.6,0.2),background_color=(0,0.2,0.8,1),background_down='atlas://data/images/defaulttheme/button')
        btn_dec = Button(text="Decrypt" , pos=(330,100) , size_hint=(0.6,0.2),background_color=(0,0.2,0.8,1),background_down='atlas://data/images/defaulttheme/button')
    
        fl = FloatLayout()
        background_image1 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(-235,0))
        background_image2 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(-2,0))
        background_image3 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(500,0))
        #box_4 = BoxLayout(size_hint=(1,0.2))
        #btn_dummy = Button()
#------------------------------------Binding Widgets-------------------------------------------------------
        file_name=['']
        btn_file_name.bind(on_press=partial(self.onClick,file_name))

        checkbox_1.bind(on_press=partial(self.EncSelect,toggle_list,0,checkbox_1,box_2))
        checkbox_2.bind(on_press=partial(self.EncSelect,toggle_list,1,checkbox_2,box_2))
        checkbox_3.bind(on_press=partial(self.EncSelect,toggle_list,2,checkbox_3,box_2))

        btn_enc.bind(on_press=partial(self.Encrypt,toggle_list,file_name))
        btn_dec.bind(on_press=partial(self.Decrypt,toggle_list,file_name))
#-------------------------------------Widgets are added----------------------------------------------------
    	
    	relative_1.add_widget(btn_file_name)
    	relative_1.add_widget(logo)
    	relative_1.add_widget(btn_header_enc)
        
        box_1.add_widget(checkbox_1)
        box_1.add_widget(checkbox_2)
        box_1.add_widget(checkbox_3)

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
        
    	fl.add_widget(background_image2)
    	fl.add_widget(background_image1)
    	fl.add_widget(background_image3)
        
        self.add_widget(fl)	
    	self.add_widget(box_outermost)

#-------------------------------------Responsive Functions-------------------------------------------------

    def Encrypt(self,*args):
            popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title_size='17sp' , size_hint=(0.555,0.2))
            bx = BoxLayout(orientation='vertical' , background_color=(0,0,0,1))
            popup_label = Label(size_hint=(1,1))
            
            keys = ['','',''] 
            children = self.children[0].children[1].children
            
            if len(args[1][0])==0:
                popup.size_hint = (0.225,0.2)
                popup.title = "Error !!" 
                popup_label.text="Please select a file !!"
                bx.add_widget(popup_label)
                popup.add_widget(bx)
                popup.open()
                return

            for c in children:
                if c.id=='0':
                    if c.text=='':
                        popup.title = "Error !!" 
                        popup_label.text="Please Enter a password for Des encryption OR deselect it !!"
                        bx.add_widget(popup_label)
                        popup.add_widget(bx)
                        popup.open()
                        return
                    keys[int(c.id)] = c.text
                elif c.id=='2':
                    if c.text=='':
                        popup.title = "Error !!" 
                        popup_label.text="Please Enter a password for Aes encryption OR deselect it !!"
                        bx.add_widget(popup_label)
                        popup.add_widget(bx)
                        popup.open()
                        return
                    keys[int(c.id)] = c.text
                elif c.id=='1':
                    keys[int(c.id)] = ' '
            if args[0].count(1)==0:
                    popup.title = "Error !!" 
                    popup.size_hint = (0.34,0.2)
                    popup_label.text = "Please Select atleast one Cipher !!"
                    bx.add_widget(popup_label)
                    popup.add_widget(bx)
                    popup.open()
                    return
            #print "python file_binary.py 'encrypt#" +args[1][0]+ "#" + json.dumps(keys) + "#" + json.dumps(args[0])+"'"
            #os.system("python file_binary.py 'encrypt#"+args[1][0]+ "#" + json.dumps(keys) + "#" + json.dumps(args[0])+"'")
            error_list = file_binary.encrypt(args[1][0] , keys ,args[0])

            if error_list[1]==1:
                f_name = args[1][0].split('.')
                self.children[0].children[0].children[0].children[0].source = f_name[0]+'.png'
                self.defaultSet(args[0])
            else :
                error_popup(error_list[0])
             
    def Decrypt(self,*args):
            popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title_size='17sp' , size_hint=(0.555,0.2))
            bx = BoxLayout(orientation='vertical')
            popup_label = Label(size_hint=(1,1))
            
            keys = ['','','']
            children = self.children[0].children[1].children
            
            if len(args[1][0])==0:
                    popup.size_hint = (0.225,0.2)
                    popup.title = "Error !!" 
                    popup_label.text="Please select a file !!"
                    bx.add_widget(popup_label)
                    popup.add_widget(bx)
                    popup.open()
                    return

            for c in children:
                if c.id=='0':
                    if c.text=='':
                        popup.title = "Error !!" 
                        popup_label.text="Please Enter a password for Des encryption OR deselect it !!"
                        bx.add_widget(popup_label)
                        popup.add_widget(bx)
                        popup.open()
                        return
                    keys[int(c.id)] = c.text
                elif c.id=='2':
                    if c.text=='':
                        popup.title = "Error !!" 
                        popup_label.text="Please Enter a password for Aes encryption OR deselect it !!"
                        bx.add_widget(popup_label)
                        popup.add_widget(bx)
                        popup.open()
                        return
                    keys[int(c.id)] = c.text
                elif c.id=='1':
                    keys[int(c.id)] = ' '
            if args[0].count(1)==0:
                    popup.title = "Error !!" 
                    popup.size_hint = (0.34,0.2)
                    popup_label.text = "Please Select atleast one Cipher !!"
                    bx.add_widget(popup_label)
                    popup.add_widget(bx)
                    popup.open()
                    return
            
            if args[0][1]==1: 
                popup = Popup(title = "Private Key" , size_hint=(0.5,0.3))

                bx = BoxLayout(orientation='vertical')
                
                submit_key = Button( text = 'Submit',size_hint=(1,0.6))
                rsa_key = TextInput(hint_text = "Enter Your Private Key" ,password=True, size_hint=(1,1))
                
                submit_key.bind(on_press=partial(self.onRsaText,args[0],args[1],keys,popup,rsa_key))
                
                bx.add_widget(rsa_key)
                bx.add_widget(submit_key)
                
                popup.add_widget(bx)
                
                popup.open()
            else:
                #dec_file_name = subprocess.check_output([sys.executable, "file_bianry.py","'decrypt#"+args[1][0]+ "#" + json.dumps(keys) + "#" + json.dumps(args[0])+"'" ])
                #dec_file_name = os.system("python file_binary.py 'decrypt#"+args[1][0]+ "#" + json.dumps(keys) + "#" + json.dumps(args[0])+"'")
                #print "dec_file_name =",dec_file_name
                error_list = file_binary.decrypt(args[1][0] , keys ,args[0])
                if error_list[1]==1:
                    self.children[0].children[0].children[0].children[0].source = error_list[0]
                    self.defaultSet(args[0])

                else:
                    self.error_popup(error_list[0])

    def error_popup(self,e):
        popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title = "Error !!",title_size='17sp' , content=Label(text=e) , size_hint=(0.5,0.5))
        popup.open()
    def onRsaText(self,*args):
        keys = args[2]
        popup = args[3]
        rsa_key = args[4]

        rsa_key = rsa_key.text
        if len(rsa_key)==0:
            popup.dismiss()
            return
        print rsa_key
        keys[1] = str(rsa_key)
        
        popup.dismiss()
        
        #dec_file_name = os.system("python file_binary.py 'decrypt#"+args[1][0]+ "#" + json.dumps(keys) + "#" + json.dumps(args[0])+"'")
        error_list = file_binary.decrypt(args[1][0] , keys ,args[0])
        if error_list[1]==1:
            self.children[0].children[0].children[0].children[0].source = error_list[0]
            self.defaultSet(args[0])
        else:
            self.error_popup(error_list[0])

    def EncSelect(self,*args):

        btn_no = args[1]
        btn_pos = [54,287,521]
        enc_type = ['Enter key for DES Encryption','','Enter key for AES Encryption']
        args[0][btn_no]=(args[0][btn_no]+1)%2
        
        if args[0][btn_no]==1:
            args[2].background_color=(0,0.2,0.8,1)
            if btn_no==1:
                return
            text_input = TextInput(id=str(btn_no),hint_text=enc_type[btn_no],password=True , pos = (btn_pos[btn_no],0) , size_hint=(0.284,1) ,background_color=(0, 0.2, 0.8, .7),hint_text_color=(1,1,1,0.7),cursor_color=(1,1,1,1),foreground_color=(1,1,1,1), background_normal='atlas://data/images/defaulttheme/button' , background_active='atlas://data/images/defaulttheme/button')
            args[3].add_widget(text_input)
        else:    
            args[2].background_color=(0,0.2,0.8,0.5)
            if btn_no==1:
                return
            children = args[3].children
            for c in children:
                if c.id==str(btn_no):
                    args[3].remove_widget(c)
        
        print args[0]

    def onClick(self,*args):
        popup = Popup(title="Load file",size_hint=(0.9, 0.9))
        fc = FileChooserIconView(rootpath='/home/john/projects/Image_encryption')
        popup.add_widget(fc)
        popup.open()
        fc.bind(on_submit=partial(self.onSubmit,fc,popup,args[0]))
    def onSubmit(self,*args):
        print args[0].selection[0]
        file_name = args[0].selection[0]
        args[1].dismiss()
        args[2][0] = file_name

        btn = self.children[0].children[3].children[1]
        
        if len(file_name)>42:
            btn.font_size='15sp'
        
        btn.valign='middle'
        btn.halign='center'
        btn.text_size = (btn.width,btn.height)
        btn.text = file_name
        self.children[0].children[0].children[2].children[0].source = file_name
        self.children[0].children[0].children[0].children[0].source = "imgz/default.jpg"

    def defaultSet(self,*args):
            self.children[0].children[3].children[1].text = "Select Image"
            self.children[0].children[3].children[1].font_size = '17sp'
            
            text_inputs = self.children[0].children[1].children
            enc_buttons = self.children[0].children[2].children

            for c in text_inputs:
                self.children[0].children[1].remove_widget(c)
            for c in enc_buttons:
                c.background_color=(0,0.2,0.8,0.5)
            args[0][0] = 0
            args[0][1] = 0
            args[0][2] = 0
    def getStats(self,*args):

class TestApp(App):
    def build(self):
        Window.size = (800, 500)
        #Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()
        
        main_screen = MainScreen(sm , name='main_screen')
        sm.add_widget(main_screen)

        return sm


if __name__=="__main__":
    TestApp().run()

