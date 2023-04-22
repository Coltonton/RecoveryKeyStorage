#!/usr/bin/python
import os, sys, time, platform, difflib, json
from os import path
from datetime import datetime
from Support.support_variables import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # __file__ is safer since it doesn't change based on where this file is called from

#########################################################
##===================== Support ====================== ##
#########################################################
def is_affirmative(key1="Yes", key2="No", output="Not Doing..."): # Ask user for confirmation
    #DebugPrint('Asking to confirm', 'sf')
    key1_l = key1.lower().strip()                   # lowercase key1 for compare
    key2_lf = key2.lower().strip()[0]               # lowercase first char key2 for compare
    key1_lf = key1_l[0] if key1_l[0] not in ["n", key2_lf] else "y" # Get first letter key1(lower), if is "n" (same as no) or same as key2 ignore...
    afirm = input('[1.{} / 2.{}]: '.format(key1,key2)).lower().strip()
    DebugPrint('Got {}'.format(afirm), 'sf')
    if ((afirm in IS_AFFIRMATIVE_YES) or (afirm in [key1_l, key1_lf])): 
        return True
    if afirm in IS_AFFIRMATIVE_UNSURE:
        print("WTF do you mean {}... I'm going to assume NO so I dont brick ya shi...".format(afirm))
    if afirm in ['i dont talk to cops without my lawyer present']: # Do you like your eggs real or plastic?
        print("Attaboy Ope!") # Please tell me you watched the Andy Griffith Show... I was only born in '99...
    
    if output != "silent": print('{}'.format(output))
    time.sleep(1.5) 
    return False

def print_text(showText, withver=0):                 # This center formats text automatically
    max_line_length = max([len(line) for line in showText]) + 4
    print(''.join(['#' for _ in range(max_line_length)]))
    for line in showText:
        padding = max_line_length - len(line) - 2
        padding_left = padding // 2
        print('#{}#'.format(' ' * padding_left + line + ' ' * (padding - padding_left)))
    print(''.join(['#' for _ in range(max_line_length)]))

def selector_picker(listvar, printtext):             # Part of @sshane's smart picker
    options = list(listvar)      # this only contains available options from self.get_available_options
    if not len(options):
        print('No options were given')
        time.sleep(2)
        return
    
    while True:
        print('\n{}'.format(printtext))
        for idx, select in enumerate(options):
            print('{}. {}'.format(idx + 1, select))
        usrinput = input("Enter Index Value: ")
        usrinput = int(usrinput)
        listlen = len(listvar)
        if usrinput <= listlen:
            usrinput -= 1
            selected_option = listvar[usrinput]
            return selected_option
        else:
            print("I\nnvalid Index... Try Again...")
    
#########################################################
##====================== Main ======================== ##
#########################################################
def get_aval_options():          # Auto discover themes and let user choose!
    DebugPrint("get_aval_themes() called", fromprocess_input="sf")
    available_options = [t for t in MAIN_OPTIONS]
    if DEVMODE:
        DebugPrint("Found all these directorys: ", multi=available_options, fromprocess_input="sf")
        #DebugPrint("Are Excluded in support.support_variables.py: ", multi=EXCLUDED_THEMES, fromprocess_input="sf")
    lower_available_themes = [t.lower() for t in available_options]
    print("\n+################################+")
    print("#            MAIN MENU           #")
    print("+################################+")
    print('What would you like to do?')

    while 1:
        for idx, option in enumerate(available_options):
            print('{}. {}'.format(idx, option))
            idx =+ 1
    
        option = input('\nChoose (by name or index): ').strip().lower()
        DebugPrint("User entered: {}".format(option), fromprocess_input="sf")
        if option in ['devmode']:
            return 'devmode'
        if option in ['exit', 'e', '0', 'stop', 0]:
            DebugPrint("Got Exit", fromprocess_input="sf")
            QUIT_PROG()
        
        if option.isdigit():
            option = int(option)
            if option == 69:
                print('nice\n')
            if option > len(available_options):
                print('Index out of range, try again!')
                continue
            return available_options[int(option)]
        else:
            if option in lower_available_themes:
                return available_options[lower_available_themes.index(option)]
            sims = [str_sim(option, t.lower()) for t in available_options]
            most_sim_idx = max(range(len(sims)), key=sims.__getitem__)
            option = available_options[most_sim_idx]
            if sims[most_sim_idx] >= MIN_SIM_THRESHOLD:
                print('Selected option: {}'.format(option))
                print('Is this correct?')
                print('[Y/n]: ', end='')
                if input().lower().strip() in IS_AFFIRMATIVE_YES:
                    DebugPrint("You entered: {}".format(input), fromprocess_input="sf")
                    return option
            else:
                print('Unknown option, try again!')
                DebugPrint("Did not match", fromprocess_input="sf")


#########################################################
## ====================== Misc ======================= ##
#########################################################
def QUIT_PROG():                # Terminate Program friendly
    print('\nThank you come again!\n\n########END OF PROGRAM########\n')
    sys.exit()  

def str_sim(a, b):              # Part of @ShaneSmiskol's get_aval_themes code
    return difflib.SequenceMatcher(a=a, b=b).ratio()

#########################################################
## ==================== DEV/Debug ==================== ##
#########################################################
def setVerbose(a=False):        #Set Verbosity (DEPRICATED)
    if a == True:
        con_output = ' >/dev/null 2>&1'  # string to surpress output
    else:
        con_output = ''  # string to surpress output
    print('[DEBUG MSG]: Verbose ' + a)

def DebugPrint(msg, fromprocess_input="null", overide=0, multi=0):  #My own utility for debug msgs
    if VERBOSE == True or DEVMODE == True or overide == 1:
        now = datetime.now()
        debugtime = now.strftime("%m/%d %I:%M.%S")
        runprocess = "main.py"
        fromprocess_input = runprocess if fromprocess_input == "null" else fromprocess_input
        if fromprocess_input == "sf":
            runprocess = (runprocess.strip(".py")+"/support/support_functions.py")

        if type(multi) == list:
            print("\n##[DEBUG][{} {}] || GOT MULTIPLE DATA".format(debugtime, runprocess))
            print("##[DEBUG] {}".format(msg))
            for x in range(len(multi)):
                print("--> {}".format(multi[x])),
        else:
            print("##[DEBUG][{} {}] || {}".format(debugtime, runprocess, msg))#] #Debug Msg ()s
