#script for whatsapp bot
version=1.0

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
     
class Wpp_bot():    
    def __init__(self):
        #gets html_info.txt elements
        txt = open("html_info.txt", "r")
        txt_list=[]
        while True:
            txt_list.append(txt.readline())
            if txt_list[-1] == "\n":
                txt_list.pop(-1)
                break
            txt_list[-1]=txt_list[-1].split("~")
        txt.close()
        self.loc={txt_list[i][0]:txt_list[i][1] for i in range(len(txt_list))}#final dict

        
        #Initiating driver, getting site, etc
        
        self.driver = webdriver.Firefox()
        self.driver.get(self.loc["url"])
        assert "WhatsApp" in self.driver.title

        #WAIT LOGGING  
        logged=False
        print("I'm loading myself!")
        while not logged:
            logged=self.exist(self.loc["pane"])
        print("I've loaded :)")
        time.sleep(1)

    #returns data=[a,b,c,...] where a,b,c... are lists [num,msg_in,pane]
    def read_new(self):
        
        #unread_items -> pane_items with unread mark
        all_panes = self.fxpath( self.loc["pane_item"] )
        unread_items=[]
        for i in range(len(all_panes)):
            if self.exist("{}[{}]{}".format(self.loc["pane_item"],i+1,self.loc["unread"])):
                unread_items.append(all_panes[i])

        data=[]
        
        #if new message
        if len(unread_items)!=0:
            for i in range(len(unread_items)):
                #PANE CLICK
                while True:
                    try:
                        unread_items[i].click()
                        break
                    except:
                        print("Unknown error")
                
                #NUM
                num = self.fxpath(self.loc["num"])
                num = num[0].text
                
                #MSG_IN
                msg_in = self.fxpath(self.loc["last_msg"])
                try:
                    msg_in = msg_in[0].text
                except:
                    msg_in=""
                print("msg_in:{}\nnum:{}\n".format(msg_in,num))

                #APPENDING                
                data.append([num,msg_in,unread_items[i]])
        return data
    
    #Simplifying#########################################################
    def fclass(self,name):#FIND CLASS - RETURN LIST
        return self.driver.find_elements_by_class_name(self.loc[name])

    def fxpath(self,name):#FIND XPATH - RETURN LIST
        if not "/" in name:
            print("esqueceu do self loc bunita")
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

    def send_to(self,string,target):#SEND TO TARGET
        try:
            self.fxpath(self.loc["pane_by_name"].format(target))[0].click()
            
        except:
            search=self.fxpath(self.loc["search"])[0]
            search.send_keys(target)

            while True:          
                try:
                    self.fxpath(self.loc["pane_by_name"].format(target))[0].click()
                    break
                except:
                    pass
            self.fxpath(self.loc["search_back"])[0].click()
                    
        if string != "":
            self.send(string)
        
    def send(self,string):#SEND TO OPENED CHAT
        if string != None:
            string=string.split("\n")
            input_box=self.fxpath(self.loc["send"])[0]
            reply=""
            for i in range(len(string)):
                reply+=string[i] + Keys.SHIFT + Keys.ENTER + Keys.SHIFT
            reply+= Keys.ENTER
            input_box.send_keys(reply)
    #######################################################################

    def send_paste(self, string):
        #ctrl v on send input
        reply = Keys.CONTROL + 'v'
        input_box=self.fxpath(self.loc["send"])[0]
        input_box.send_keys(reply)

        #writes and send subtitle
        while True:
            input_box_list = self.fxpath(self.loc["img_subtitle"])
            if(len(input_box_list)>0):
                break
            
        input_box = input_box_list[0]
        reply = string
        reply += Keys.ENTER
        input_box.send_keys(reply)

        #writes and send subtitle
        while True:
            input_box_list = self.fxpath(self.loc["send"])
            if(len(input_box_list)>0):
                break
            
    def refresh(self):
        data=self.read_new()
        
        

bot=Wpp_bot()
while True:
    answer = input("press ENTER key to send and image or any other key to leave")
    if len(answer)!=0:
        break
    
    bot.send_paste("testing")
        

    

        


                



