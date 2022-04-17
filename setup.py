"""
a script to set up the whole bot. Take command line inputs and add them into a json
file as login information.

this script also will write the necessary files for the thing to run.
"""
import os
import json
from time import sleep
from tkinter import Y
from webbrowser import open_new

def obtainToken():
   user_prompt = "\n\033[1;37;40mCopy and paste the token right here below.\n\n\t\033[1;36;40mToken: \033[0;37;40m" 
   token = input(user_prompt)
   return token

def obtainPassword():
    PW_prompt = '\n\033[1;37;40mEnter password for login\n\n\t\033[1;36;40mPassword: \033[0;37;40m'
    password_input = input(PW_prompt)
    return password_input

def writeSetup(token, password):
    creds = {
        "token" : token,
        "password" : str(password),
    }

    # Serializing json 
    json_object = json.dumps(creds, indent = 4)
    
    # Writing to sample.json
    with open("setup.json", "w") as outfile:
        outfile.write(json_object)
        

    print("\n\033[1;37;40mYour credentials for the bot have been set up.\033[0;37;40m\n")
    print("\n\033[1;37;40mYou can always manually edit the \"setup.json\" file to make changes.\033[0;37;40m\n")


def main():
    
    startLines = [
        "\n\033[1;37;40mWelcome to Self-bot for \033[1;36;40mGroupMe\033[1;37;40m setup\033[0;37;40m\n",
        "\n\033[1;37;40mYou can always run this file again to change anything. \033[0;37;40m\n",
    ]

    os.system('cls')
    for line in startLines:
        print(line)
        sleep(2.0)

    token_prompt = "\n\033[1;37;40mDid you obtain a user token from \033[1;36;40mGroupMe\033[1;37;40m? [Y/n]: \033[0;37;40m"
    if input(token_prompt) == 'Y':
        token = obtainToken()
        
    else:
        print("\n\033[1;37;40mYou can obtain a user token from \033[1;36;40mGroupMe\033[1;37;40m.\033[0;37;40m\n")
        redirect_prompt = "\n\033[1;37;40mWould you like to be redirected to where you can get your token? [Y/n]: \033[0;37;40m"
        if input(redirect_prompt) == 'Y':
            print("\n\033[1;37;40mLogin with your credentials in the website to obtain your token.\033[0;37;40m\n")
            sleep(1.0)
            open_new("https://dev.groupme.com/")
            token = obtainToken()
        else:
            print("\n\033[1;37;40mYou can always manually enter your token in the \"setup.json\" file.\033[0;37;40m\n")
            if input("\n\033[1;37;40mEnter [0] to exit now and come back later, or [1] to redirect to GroupMe : \033[0;37;40m") == '0':
                exit()
            else:
                open_new("https://dev.groupme.com/")
                token = obtainToken()

    password = obtainPassword()
    

    writeSetup(token,password)

            

main()