#script for whatsapp bot
version=1.0

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
     
class Wpp_bot():    
    def __init__(self):
        #gets html_info.txt xpath to elements
        txt = open("html_info.txt", "r")
        txt_list = []
        while True:
            txt_list.append(txt.readline())
            if txt_list[-1] == "\n":
                txt_list.pop(-1)
                break
            txt_list[-1]=txt_list[-1].split("~")
        txt.close()
        self.xpath_dict={txt_list[i][0]:txt_list[i][1] for i in range(len(txt_list))}#final dict

        
        #Initiating driver, getting site, etc
        
        self.driver = webdriver.Firefox()
        self.driver.get(self.xpath_dict["url"])
        assert "WhatsApp" in self.driver.title

        #WAIT LOGGING  
        logged=False
        print("Code initialized, waiting for the chat page to load")
        while not logged:
            logged=self.exist(self.xpath_dict["pane"])
        print("Chat page loaded")
        time.sleep(1)
    

    def fclass(self,name):#FIND CLASS - RETURN LIST
        return self.driver.find_elements_by_class_name(self.xpath_dict[name])

    def fxpath(self,name):#FIND XPATH - RETURN LIST
        return self.driver.find_elements_by_xpath(name)

    def get_at(self,elements,at):#GET ATTRIBUTES FROM ELEMENTS
        l=[]
        for i in elements:
            l.append(i.get_attribute(at))
        return l
    
    def exist(self,xpath):#WETHER XPATH EXISTS OR NOT -> boolean
        try:
            self.driver.find_element_by_xpath(xpath)
            exist=True
        except:
            exist=False
        return exist

    #search for certain chat then sends message
    def send_to(self, string, target):
        try:
            self.fxpath(self.xpath_dict["pane_by_name"].format(target))[0].click()
            
        except:
            search=self.fxpath(self.xpath_dict["search"])[0]
            search.send_keys(target)

            while True:          
                try:
                    self.fxpath(self.xpath_dict["pane_by_name"].format(target))[0].click()
                    break
                except:
                    pass
            self.fxpath(self.xpath_dict["search_back"])[0].click()
                    
        if string != "":
            self.send(string)

    #sends message to openned chat
    def send(self,string):
        if string != None:
            string=string.split("\n")
            input_box=self.fxpath(self.xpath_dict["send"])[0]
            reply=""
            for i in range(len(string)):
                reply+=string[i] + Keys.SHIFT + Keys.ENTER + Keys.SHIFT
            reply+= Keys.ENTER
            input_box.send_keys(reply)

    #sends image from clipboard and then writes custom subtitle, then sends to openned chat.
    def send_paste(self, string=""):
        #ctrl v on send input
        reply = Keys.CONTROL + 'v'
        input_box=self.fxpath(self.xpath_dict["send"])[0]
        input_box.send_keys(reply)

        #writes and send subtitle
        while True:
            input_box_list = self.fxpath(self.xpath_dict["img_subtitle"])
            if(len(input_box_list)>0):
                break
            
        input_box = input_box_list[0]
        reply = string
        reply += Keys.ENTER
        input_box.send_keys(reply)

        #writes and send subtitle
        while True:
            input_box_list = self.fxpath(self.xpath_dict["send"])
            if(len(input_box_list)>0):
                break
            

        
        

bot = Wpp_bot()
input("press enter to send a message to openned chat")
bot.send("This message was automatically sent")
input("press enter to send an image from your clipboard")
bot.send_paste("This subtitle was automatically sent")
        

    

        


                



