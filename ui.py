#!/usr/bin/env python

import math
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
        
        btn_file_name = Button(text='Select Image' ,background_down=self.popup_back, pos=(200,0) , font_size = '17sp', size_hint=(0.5,0.2),background_color=(0,0.2,0.8,1))
        logo = Image(source='imgz/logo_1.png' , pos=(77,45) , size_hint=(0.8,0.8))
        btn_header_enc = Button(text='Ciphers' , pos=(50,-58) , font_size = '17sp', size_hint=(0.875,0.2),background_color=(0,0.2,0.8,4),disabled=True , disabled_color=(1,1,1,1))

        box_1 = BoxLayout(orientation='horizontal',size_hint=(1,0.5),padding=(50,0),spacing=(2))
        toggle_list = [0,0,0]
        checkbox_1 = Button(text="DES", font_size = '17sp',background_down=self.popup_back,size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5))
        checkbox_2 = Button(text="RSA", font_size = '17sp',background_down=self.popup_back,size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5))
        checkbox_3 = Button(text="AES", font_size = '17sp',background_down=self.popup_back,size_hint=(1,0.4),background_color=(0,0.2,0.8,0.5))

       
        Box_2 = BoxLayout(orientation='horizontal',size_hint=(1,0.5))
        box_2 = RelativeLayout(orientation='horizontal',size_hint=(1,0.15))

        box_3 = BoxLayout(orientation='horizontal' , padding=(10,10))
        float_1 = BoxLayout()
        float_2 = FloatLayout()
        float_3 = BoxLayout()
        
        src_img = Image(id = 'src_img' , source = 'imgz/default.jpg',size_hint=(1,1))
        dest_img = Image(id = 'dest_img' , source = 'imgz/default.jpg',size=(1,1))
        btn_enc = Button(text="Encrypt" ,background_down=self.popup_back, pos=(330,50) , size_hint=(0.6,0.2),background_color=(0,0.2,0.8,1))
        btn_dec = Button(text="Decrypt" ,background_down=self.popup_back, pos=(330,100) , size_hint=(0.6,0.2),background_color=(0,0.2,0.8,1))
    
        fl = FloatLayout()
        background_image1 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(-235,0))
        background_image2 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(-2,0))
        background_image3 = Image(source = 'imgz/background.jpg' , allow_strech=True , size_hint=(1,1) , pos=(500,0))

#------------------------------------Binding Widgets-------------------------------------------------------
        file_name=['']
        btn_file_name.bind(on_release=partial(self.onClick,file_name))

        checkbox_1.bind(on_release=partial(self.EncSelect,toggle_list,0,checkbox_1,box_2))
        checkbox_2.bind(on_release=partial(self.EncSelect,toggle_list,1,checkbox_2,box_2))
        checkbox_3.bind(on_release=partial(self.EncSelect,toggle_list,2,checkbox_3,box_2))

        btn_enc.bind(on_release=partial(self.Encrypt,toggle_list,file_name))
        btn_dec.bind(on_release=partial(self.Decrypt,toggle_list,file_name))

#-------------------------------------Widgets are added----------------------------------------------------    	
    	relative_1.add_widget(logo)
    	relative_1.add_widget(btn_file_name)
    	relative_1.add_widget(btn_header_enc)
        
        box_1.add_widget(checkbox_1)
        box_1.add_widget(checkbox_2)
        box_1.add_widget(checkbox_3)

        float_1.add_widget(src_img)
        float_2.add_widget(btn_enc)
        float_2.add_widget(btn_dec)
        float_3.add_widget(dest_img)

        box_3.add_widget(float_1)
        box_3.add_widget(float_2)
        box_3.add_widget(float_3)

        box_outermost.add_widget(relative_1)
        box_outermost.add_widget(box_1)
        box_outermost.add_widget(box_2)
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
                    keys[int(c.id)] = ''
            if args[0].count(1)==0:
                    popup.title = "Error !!" 
                    popup.size_hint = (0.34,0.2)
                    popup_label.text = "Please Select atleast one Cipher !!"
                    bx.add_widget(popup_label)
                    popup.add_widget(bx)
                    popup.open()
                    return
            
            if args[0][1]==1:
            	popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title = "Public Key",title_size='17sp', size_hint=(0.28,0.5),separator_color=(1,1,1,0.7))

                bx = BoxLayout(orientation='vertical')
                
                submit_key = Button( text = 'Submit',background_color=(0,0.2,0.8,100),background_down=self.popup_back,size_hint=(1,0.2))
                rsa_key = TextInput(hint_text = "Enter Your Public Key OR Submit an empty field to generate new public and private keys" , font_size='17.2sp',line_spacing=-4 , padding=(12,0) ,password=True, size_hint=(1,1))
                
                submit_key.bind(on_release=partial(self.onRsaText,args[0],args[1],keys,popup,rsa_key,'encrypt'))
                
                bx.add_widget(rsa_key)
                bx.add_widget(submit_key)               
               	popup.add_widget(bx)
  
                popup.open()
            
            else :
				error_list = file_binary.encrypt(args[1][0] , keys ,args[0])
				
				if error_list[1]==1:
					if args[0][1]==1:
						print error_list[0]
						self.displayRsa(error_list[0])
					f_name = args[1][0].split('.')
					self.children[0].children[0].children[0].children[0].source = f_name[0]+'.png'
					self.getStats(args[1][0],f_name[0]+".png",error_list[2],args[0],"encrypt")
					self.defaultSet(args[0],args[1])
				
				else:
					self.error_popup(error_list[0])
             
    def Decrypt(self,*args):
            popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title_size='17sp',separator_color=(1,1,1,0.7) , size_hint=(0.555,0.2))
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
                popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title = "Private Key",title_size='17sp', size_hint=(0.28,0.5),separator_color=(1,1,1,0.7))

                bx = BoxLayout(orientation='vertical')
                
                submit_key = Button( text = 'Submit',background_color=(0,0.2,0.8,100),background_down=self.popup_back,size_hint=(1,0.2))
                rsa_key = TextInput(hint_text = "Enter Your Private Key" , font_size='17.2sp',line_spacing=-4 , padding=(12,0) ,password=True, size_hint=(1,1))
                
                submit_key.bind(on_release=partial(self.onRsaText,args[0],args[1],keys,popup,rsa_key , 'decrypt'))
                
                bx.add_widget(rsa_key)
                bx.add_widget(submit_key)    
                popup.add_widget(bx)
                
                popup.open()
            else:
                error_list = file_binary.decrypt(args[1][0] , keys ,args[0])
                if error_list[1]==1:
                    self.children[0].children[0].children[0].children[0].source = error_list[0]
                    self.getStats(args[1][0],error_list[0],error_list[2],args[0],"decrypt")
                    self.defaultSet(args[0],args[1])

                else:
                    self.error_popup(error_list[0])

    def error_popup(self,e):
        popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title = "Error !!",title_size='17sp',separator_color=(1,1,1,0.7) , content=Label(text=e) , size_hint=(0.5,0.5))
        popup.open()
    def onRsaText(self,*args):
        keys = args[2]
        popup = args[3]
        rsa_key = args[4]

        rsa_key = rsa_key.text
        if len(rsa_key)==0 and args[5]=='decrypt':
            popup.dismiss()
            return
        rsa_key = rsa_key.replace('\n','')
        print rsa_key
        keys[1] = str(rsa_key)
        
        popup.dismiss()
        
        if args[5]=='decrypt':
        	error_list = file_binary.decrypt(args[1][0] , keys ,args[0])
        elif args[5]=='encrypt':
			error_list = file_binary.encrypt(args[1][0] , keys ,args[0])

        if error_list[1]==1:
			if args[5]=='decrypt' :
				self.children[0].children[0].children[0].children[0].source = error_list[0]
				self.getStats(args[1][0],error_list[0],error_list[2],args[0],"decrypt")
			else:
				if keys[1]=='':
					if args[0][1]==1:
						print error_list[0]
						self.displayRsa(error_list[0])
				f_name = args[1][0].split('.')
				self.children[0].children[0].children[0].children[0].source = f_name[0]+'.png'
				print "Timing Array = ",error_list[2]
				self.getStats(args[1][0],f_name[0]+".png",error_list[2],args[0],"encrypt")
			self.defaultSet(args[0],args[1])
        else:
            self.error_popup(error_list[0])

    def EncSelect(self,*args):

        btn_no = args[1]
        btn_pos = [50,287,518]
        enc_type = ['Enter key for DES Encryption','','Enter key for AES Encryption']
        args[0][btn_no]=(args[0][btn_no]+1)%2
        
        if args[0][btn_no]==1:
            args[2].background_color=(0,0.2,0.8,1)
            if btn_no==1:
                return
            text_input = TextInput(id=str(btn_no),hint_text=enc_type[btn_no],password=True , pos = (btn_pos[btn_no],0) , size_hint=(0.290,1) ,background_color=(0, 0.2, 0.8, .7),hint_text_color=(1,1,1,0.7),cursor_color=(1,1,1,1),foreground_color=(1,1,1,1), background_normal='atlas://data/images/defaulttheme/button' , background_active='atlas://data/images/defaulttheme/button' , multiline=False)
            args[3].add_widget(text_input)
        else:    
            args[2].background_color=(0,0.2,0.8,0.5)
            if btn_no==1:
                return
            children = args[3].children
            for c in children:
                if c.id==str(btn_no):
                    args[3].remove_widget(c)
        
    
    def onClick(self,*args):
        popup = Popup(background='imgz/back_blue_1.jpg',background_color = (0,0,0,0.6),title_size='17sp' ,title="Load file",size_hint=(0.8, 0.8),separator_color=(1,1,1,0.7))
        fc = FileChooserIconView(path='/home/john/projects/Image_encryption')
        popup.add_widget(fc)
        popup.open()
        fc.bind(on_submit=partial(self.onSubmit,fc,popup,args[0]))
    
    
    def onSubmit(self,*args):
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
            
            args[1][0] = ""
            self.children[0].children[3].children[1].text = "Select Image"
            self.children[0].children[3].children[1].font_size = '17sp'
            
            text_inputs = self.children[0].children[1].children
            enc_buttons = self.children[0].children[2].children
            
            for c in range(len(text_inputs)):
                self.children[0].children[1].remove_widget(text_inputs[0])
            for c in enc_buttons:
                c.background_color=(0,0.2,0.8,0.5)
            
            args[0][0] = 0
            args[0][1] = 0
            args[0][2] = 0
    
    
    def getStats(self,*args):
        cipher_list = ["DES","RSA","AES"]

        inp_file_size = os.path.getsize(args[0])
        out_file_size = os.path.getsize(args[1])

        inp_file_name = args[0].split('/')[-1]
        out_file_name = args[1].split('/')[-1]

        to_disp = "Input File     :\n    Name - "+inp_file_name+"\n    Size    - "+str(inp_file_size)+" Bytes "
        to_disp += "\n\nOutput File   :\n    Name - "+out_file_name+"\n    Size    - "+str(out_file_size)+" Bytes "
        to_disp += "\n\nTime Taken  : "
        
        if args[4]=="encrypt" or len(args[2])==2:
            j=0
        else:
            j=2
        
        i=0
        for c in args[3]:
            if c==1:
                to_disp += "\n    "+cipher_list[j]+" -  "+str(math.ceil(args[2][i]*10000)/10000)+"s"
                i+=1
            if args[4]=="encrypt" or len(args[2])==2:
                j+=1
            else:
                j-=1

        to_disp += "\n\nTotal Time    :  "+str(math.ceil(args[2][i]*10000)/10000)+"s"

        popup = Popup(background=self.popup_back,background_color = (0,0,0,0.6),title_size='17sp' ,title="Stats" , size_hint=(0.4,0.65),separator_color=(1,1,1,0.7))
        label = Label(text=to_disp)
        popup.add_widget(label)
        popup.open()
    
    
    def displayRsa(self,*args):
    	popup_title = "Private Key for RSA                    Public Key for RSA"
        popup = Popup(title=popup_title,background=self.popup_back,background_color = (0,0,0,0.6),size_hint = (0.6,0.6),title_size='17sp',separator_color=(1,1,1,0.7))
       
       	bx = BoxLayout(orientation='horizontal')
        bx1 = BoxLayout(orientation='vertical')
        btn_copy = Button(text="Copy",background_down=self.popup_back,background_color=(0,0.2,0.8,100),color=(1,1,1,1),size_hint=(1,0.2))

        print args
        
        rsa_key = ''
        for i in range(len(args[0][0])):
            if i%25==0 and i!=0:
                rsa_key += '\n'
                rsa_key += args[0][0][i]
            else:
                rsa_key += args[0][0][i]

        label = TextInput(text = rsa_key,readonly=True,auto_indent=True,strip=True)

        btn_copy.bind(on_release=partial(self.copy,rsa_key,label))
        
        bx1.add_widget(label)
        bx1.add_widget(btn_copy)
        
        bx2 = BoxLayout(orientation='vertical')
        btn_copy = Button(text="Copy",background_down=self.popup_back,background_color=(0,0.2,0.8,100),color=(1,1,1,1),size_hint=(1,0.2))

        print args
        
        rsa_key = ''
        for i in range(len(args[0][1])):
            if i%25==0 and i!=0:
                rsa_key += '\n'
                rsa_key += args[0][1][i]
            else:
                rsa_key += args[0][1][i]

        print rsa_key
        
        label = TextInput(text = rsa_key,readonly=True,auto_indent=True,strip=True)

        btn_copy.bind(on_release=partial(self.copy,rsa_key,label))
        
        bx2.add_widget(label)
        bx2.add_widget(btn_copy)
       	
       	bx.add_widget(bx1)
       	bx.add_widget(bx2)
        popup.add_widget(bx)
        
        popup.open()

    def copy(self,*args):
        args[1].copy(data=args[0])


class FinalApp(App):
    def build(self):
        Window.size = (800, 500)
        
        self.title = "Image Encryption"
        
        sm = ScreenManager()
        
        main_screen = MainScreen(sm , name='main_screen')
        
        sm.add_widget(main_screen)
        return sm

if __name__=="__main__":
    FinalApp().run()

