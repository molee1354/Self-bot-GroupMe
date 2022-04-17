import os
import json
from getpass import getpass

def login():
    os.system('pip install GroupyAPI')
    os.system('pip install tkinter')
    os.system('cls')

    with open('setup.json', 'r') as f:
        creds = json.load(f)

    # #! change token filename to wherever the token is
    # token_filename = 'token.txt'

    # token_filename = 'tokenRobert.txt'
    prompt = '\n\033[1;37;40mEnter Password to Login: \033[0;37;40m'

    #getting user password
    pw = getpass(prompt = prompt)
    
    if pw == creds["password"]:
        print('\n\033[1;36;40mLogin Successful!\033[0;37;40m\n')
        # with open(token_filename,'r') as t:
        #     token = t.readline()
            # print(token)
        token = creds["token"]
        return token
    else:
        print('\n\033[1;31;40mWrong Password\033[0;37;40m\n')
        pw = None
        exit()

