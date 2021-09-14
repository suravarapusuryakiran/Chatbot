# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from actions.language import get_languages, check_product
from actions.validation import validation
from actions.product_info import product_info
from numpy import product
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from tests.cad_downloader import download_CAD
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import os
import pickle
import pandas as pd
import urllib
import shutil
pd.set_option('display.max_colwidth', None)



class ValidateCadForm(Action):
    def name(self) -> Text:
        return "validate_cad_form"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        required_slots = ["what", "code"]
        if tracker.get_slot('what') == "sheet":
            required_slots.append("language")

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                return [SlotSet("requested_slot", slot_name)]

        return [SlotSet("requested_slot", None)]


class ActionButton(Action):
    def name(self) -> Text:
        return "action_button"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons=[
            {"payload": '/intent_what_without_code{"what":"cad"}', "title": "CAD"},
            {"payload": '/intent_what_without_code{"what":"sheet"}', "title": "Data Sheet"}
        ]
        dispatcher.utter_message(text="What do you need?", buttons=buttons) 
        return[]

class ActionAskLanguage(Action):
    def name(self) -> Text:
        return "action_ask_language"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code_entered = tracker.get_slot('code').upper()

        if "CGT3" in code_entered:
            product_group_check = True
        else:
            product_group_check,code_entered = check_product(code_entered) 

        print(product_group_check) # True or false
        print(code_entered)         # cytropac
        
        if product_group_check:
            buttons = []
            languages = get_languages(code_entered)
            for language in languages:
                buttons.append({"payload": '/intent_language{"language":"' + language + '"}', "title": language.title()})

            if len(buttons):
                print("Entered into true condition of buttons")
                dispatcher.utter_message(text="In which language you want Data Sheet?", buttons=buttons)
            else:
                print("Currently, we couldn't provide any datasheet for this product.!")
                dispatcher.utter_message(f"Currently, we couldn't provide any datasheet for this product.!")

            
            return[]
        else:
            dispatcher.utter_message(f"Entered code seems to be invalid, Please check and enter valid code again!")
            return[]
        
class ActionHey(Action):
    global mydownload_file 

    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("actions triggered")
        
        intent = tracker.get_slot('what')
        code = tracker.get_slot('code') 
        User_Entered_code=code.upper()
        language = tracker.get_slot('language')
        con_id= tracker.sender_id

        valid_code = validation(User_Entered_code)
        df, material_number, type_code = valid_code[0],valid_code[1],valid_code[2]
        print(df)
        print(f" material number is {material_number}")
        print(f" typecode is {type_code}")

        if intent == 'cad':

            dispatcher.utter_message(f"We are working on CAD for {User_Entered_code}")    
            if User_Entered_code.startswith("CGT3"):
                product = "CGT3"
                product_group = "Hydraulic cylinder - Tie rod design"  # typecode starts with CG always redirects to cylinders.!!!!
                product_img = "https://www..jpg"
                link= "https://www.&Typecode=dankeschöne&InitConfiguration=1&o=Desktop"
                url= link.replace('dankeschöne',User_Entered_code)
                dispatcher.utter_message(image= product_img)
                dispatcher.utter_message(f"Entered code refers to product {product} family. \n {product_group} \n")
                dispatcher.utter_message(response="utter_link", link=url)

            else:

                if df.empty:
                    flag= False
                    dispatcher.utter_message(f"Entered code seems to be invalid, Please check and enter valid code again!")
                else:
                    flag=True
                    # print("Entered typecode is valid")

                if flag is True:
                    status,filepath=download_CAD(material_number)

                    if status is False:
                        dispatcher.utter_message(f"Entered code is valid but CAD is not Available!")
                    else:
                        #dispatcher.utter_message(image= product_img)
                        #dispatcher.utter_message(f"Entered code refers to product {product} family. \n Material number: {material_number} \n Typecode: {type_code} ")
                        p=os.path.dirname(os.path.dirname( __file__ ))
                        userfile=os.path.join(p+"/"+filepath)
                        print(" file location -->" + userfile)
                        Userpath=os.path.join("/mnt/c/work/usu1lo/spyderPro/customer_files/" +con_id + "/")
                        #"/mnt/c/work/usu1lo/spyderPro/customer_files/"
                        if not os.path.exists(Userpath):
                            os.mkdir(Userpath)
                        shutil.copy(userfile, Userpath)
                        global mydownload_file
                        mydownload_file= filepath
                        print("file name ->" + mydownload_file )
                        filename=os.path.basename(filepath) 
                        webUrl="http://localhost:5012/download" +"?" + "con_id=" + con_id + "&filename=" + filename 
                        dispatcher.utter_message(response="utter_cadlink", link=webUrl)
                        #dispatcher.utter_message(attachment="datasheets.xlsx")
                else:
                    pass                

        elif intent == 'sheet':
            # provide the links 
            # we already know language (language) and based on typecode we know product, so provide links to that product and language
            dispatcher.utter_message(f"We are working on Data Sheet for {User_Entered_code}")

            product_details = product_info(User_Entered_code)
            print(product_details)
            product = product_details['baureihe'].upper() # CYTROPAC
            product_img = product_details['img_loc']
            print(product)
            # webUrl=mydf.loc[mydf['product']==product][language].to_string(index=False)
            print(language)
            webUrl=product_details[language]
            dispatcher.utter_message(image= product_img)
            dispatcher.utter_message(f"Entered code refers to product {product} family.")
            if bool(webUrl):
                dispatcher.utter_message(response="utter_link", link=webUrl)
            else:
                dispatcher.utter_message("Currently, we couldn't provide any datasheet for this product.!")

        else:
            dispatcher.utter_message(f"Sorry, We can't help you with that!")
