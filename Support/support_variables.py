#!/usr/bin/python
# ===================  Misc vars =================== ##
RECOVERYKEYSTORAGE_VER = "dev"              # This Softwares Version
VERBOSE = True
DEVMODE = False
DEV_PLATFORM = ""
IS_AFFIRMATIVE_YES = ['yes', 'ye', 'y', '1', "j", "ja", "si", "s"]
IS_AFFIRMATIVE_UNSURE = ['i guess', 'sure', 'fine', 'whatever', 'idk', 'why', "uh", "um", "...", "bite me", "eat my shorts"]
MIN_SIM_THRESHOLD = 0.25      # user's input needs to be this percent or higher similar to a theme to select it
MAIN_OPTIONS = ["Terminate Program","Use a key"] # "Add a key", "Delete a key"
NEW_LINE_STAR = "\n*\n"
REC_KEYS_LOC = 'Files/keys.json'

# ===================== Texts ====================== ##
WELCOME_TEXT = ['Created By: Colton (Brandon) S. EndLine \\n',
                'Free to use! Free to Edit! Free to integrate!',
                'Tool for securing recovery keys!',
                ' ',
                'Version {}'.format(RECOVERYKEYSTORAGE_VER)]