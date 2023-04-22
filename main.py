import time, os
from os import path
from Support.support_functions import * 
from Support.support_variables import *
from cryptography.fernet import Fernet #pip3 install cryptography
import json


######################################################################################################
##======================= CODE START ================================================================#
######################################################################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))  # __file__ is safer since it doesn't change based on where this file is called from

class RecoveryKeys:
    def __init__(self):             # Init code runs once. sets up
        print_text(WELCOME_TEXT)          # Print welcome text with the flag for self welcome text
        DebugPrint("VERBOSE MODE ON")     # Notify if Verbosity Mode is on, DebugPrints only run in dev or verbose mode
        self.loop()                 # Do Loop                                             

    def loop(self):                 # Loop
        while True:
            #self.use_key()
            #selector_picker(["Add a key", "Use a key", "Delete a key"], "What Would You Like To Do?")
            chosenoption = get_aval_options()
            if chosenoption == "Add a key":
                self.add_key()
            elif chosenoption == "Use a key":
                self.use_key()
            elif chosenoption == "Delete a key":
                self.rem_key()
            else:
                print("RETURNED INVALID")

    def add_key(self):              # Add a Key
        pass
        name = input("What key is this for?")
        howmany = input("How Many Keys? ")
        import json
        f = open('Files/keys.json')
        
        # returns JSON object as 
        # a dictionary
        jsonData = json.load(f)
        
        # Iterating through the json
        # list
        for i in jsonData['apple']:
            print(i)
            break
        
        # Closing file
        f.close()

    def use_key(self):              # Use a Key
        fi = ""
        usedKeyPairs = 0
        codeFound = False
        try:
            fi = open(REC_KEYS_LOC)
        except FileNotFoundError:
            print("FileNotFoundError: ({}) Not found...".format(REC_KEYS_LOC))
            QUIT_PROG()
        except:
            print("A file exception occurred...") 
            QUIT_PROG()
        else:
            jsonData = json.load(fi)
            fi.close()

        # Ask User For Account
        while True:   
            selectedAccount = input("{}For which account? #".format(NEW_LINE_STAR))
            #usrinput = 'a'
            DebugPrint("User Entered: {}".format(selectedAccount))
            try:
                totalKeyPairs = len(jsonData[selectedAccount][0]["Keys"])
            except KeyError:
                print("KeyError '{}' Not Found".format(selectedAccount))
            except:
                print("An exception occurred... Try Again")
            else:
                accountAmount = len(jsonData)
                temp = list(jsonData.items())
                selectedAccountIdx = [idx for idx, key in enumerate(temp) if key[0] == selectedAccount][0]
                availableKeyPairs = totalKeyPairs

                DebugPrint("var.selectedAccount = {}".format(selectedAccount))
                DebugPrint("var.selectedAccountIdx = {}".format(selectedAccountIdx))
                DebugPrint("var.accountAmount = {}".format(accountAmount))
                DebugPrint("var.totalKeyPairs = {}".format(totalKeyPairs))
                break

        # Get An Unused Key Value
        while True:   
            GetRecoveryCode = jsonData[selectedAccount][0]["Keys"][availableKeyPairs-1]['recovery{}'.format(availableKeyPairs)]
            DebugPrint("Trying var.GetRecoveryCode = recovery{}".format(availableKeyPairs))
            if GetRecoveryCode[0:4] == "used":
                DebugPrint("# USED: recovery{} Searching for next".format(availableKeyPairs))
                availableKeyPairs -= 1
                usedKeyPairs += 1 
                DebugPrint("# var.availableKeyPairs = {} & var.usedKeyPairs = {}".format(availableKeyPairs, usedKeyPairs))
            else:
                DebugPrint("# FOUND: recovery{} has not been used, and is {}".format(availableKeyPairs, GetRecoveryCode))
                selectedRecoveryKey = availableKeyPairs
                selectedRecoveryKeyIdx = availableKeyPairs-1
                DebugPrint("# var.availableKeyPairs = {} & var.usedKeyPairs = {}".format(availableKeyPairs, usedKeyPairs))
                print("\n###\n# {}/{} keys are now used, {} more available.".format(usedKeyPairs+1, totalKeyPairs, availableKeyPairs-1))
                
                if availableKeyPairs-1 == 0:
                    print("# WARNING ALL RECOVERY KEYS USED GENERATE MORE IMMEDIATELY!!!!")
                elif ((totalKeyPairs-usedKeyPairs) <=2):
                    print("# WARNING consider generating more!")
                print("#\n# Your recovery code is {}\n# Press Enter To Continue...".format(GetRecoveryCode))
                input("###")
                break
            if availableKeyPairs == 0:
                print("\nYOU IDIOT! YOU HAVE NO VALID RECOVERY CODES IN THE DATABASE!! CONTACT SUPPORT AND PRAY!!\n")
                QUIT_PROG()

        usedKeyOutput = "used" if DELETE_AFTER_USE else "used.{}".format(GetRecoveryCode)
        jsonData[selectedAccount][0]["Keys"][selectedRecoveryKeyIdx] = {"recovery{}".format(selectedRecoveryKey): "{}".format(usedKeyOutput)}
        DebugPrint("Outfile data = \n{}".format(jsonData))
        file = open(REC_KEYS_LOC, 'w')
        json.dump(jsonData, file, indent=3)
        file.close()

    def rem_key(self):              # Remove a Key
        pass


if __name__ == '__main__':
    rk = RecoveryKeys()