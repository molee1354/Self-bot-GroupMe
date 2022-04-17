import os
from random import randint
import login
from datetime import datetime 
from tkinter import Label, Tk, Button


#* the features right now are searching the web (urls), and wordle.
from websearch import websearch
from wordle import wordle_run

#setting up the token
token = login.login()

#todo exception for no module
try: 
    from groupy.client import Client
    client = Client.from_token(token)
except ModuleNotFoundError:
    print("The module was not found. Try \'pip install GroupyAPI\' on the command line.")
    exit()

#your first name is the name of your bot
self_info = client.user.get_me()
self_name = self_info['name']

# * function to select channel
def channel_Menu():
    os.system('cls')

    def channel_select(channelName):

        #listing all the groups
        for number,group in enumerate(client.groups.list()):
            if number == int(channelName)-1:
                # print('Current Channel:',group.name)
                return group

    # * command line output                
    print('\033[1;37;40mAvailable Channels\033[0;37;40m\n')
    for idx, group in enumerate(client.groups.list()):
        print('\033[1;36;40m[%d]  \033[1;37;40m%-30s\033[0;37;40m' % (idx+1,group.name))
    print('\n\033[1;31;40m[%d]  \033[1;37;40m%-30s\033[0;37;40m' % (0,'Exit'))    

    #user input
    command_input = input('\n\033[1;35;40m[INPUT CHANNEL NUMBER] \033[0;37;40m>>>  ')

    #exit case
    if int(command_input) == 0:
        exit()

    try:
        channel = channel_select(command_input)
    except ValueError or UnboundLocalError:
        channel_Menu()

    return channel

#* function to set cout font color to cyan
def setCyan(text):
    #set cyan is 36
    return '\033[1;36;40m'+text+'\033[0;37;40m'

#* send message function
def send_message(words):
    channel.post(text = words)

#* send picture function
def send_picture(picture_filename):
    with open(picture_filename, 'rb') as f:
        urls = client.images.upload(f)
    
    send_message(urls['picture_url'])

# * Functions to like/unlike the most recent message
def like_recent_message():
    #most recent message
    message_choice = lines[1]
    message_choice.like()
    

#* update function
def update(user_message):
    os.system('cls')
    print('\033[1;37;40mCurrent Channel: {}\033[0;37;40m'.format(group_to_pick))
    print('')

    #message lines
    global lines
    global recentMessage
    lines = channel.messages.list()
    
    #the most recent message
    recentMessage = lines[0]

    lines = lines[:2]

    for idx,line in enumerate(reversed(list(lines))):
        cout = '\033[1;36;40m[%02d]\033[1;37;40m%18s\033[0;37;40m :  %s' % (idx+1,line.name,line.text)
        
        #todo change this to self-name
        if line.name == self_name:
            cout = '\033[1;36;40m[%02d]\033[1;33;40m%18s\033[0;37;40m :  %s' % (idx+1,line.name,line.text)

        print(cout)

    print('\033[1;37;40m'+user_message+'\033[0;37;40m')


#* run bot function
def run_bot():

    global user_message
    global nowTxt

    #! the words list
    bad_words = [
        #todo more to be added
    ]
    with open('bad_word_list.txt', 'r') as f:
        badwordLines = f.readlines()
        words = []
        for line in badwordLines: 
            word = line.strip()
            bad_words.append(word)

    #the names of the people who are exempt from censoring
    bad_word_exemptions = [
        #firstname lastname,
        self_name,
    ]

    #function to look for swear words --> return true if bad word found
    def findBadWord(words):
        for word in words:
            if word.lower() in bad_words:
                return True

        return False

    #setting the basic update message
    dt = datetime.now()
    nowTxt = dt.strftime("%m/%d %H:%M:%S")
    timeTxt = dt.strftime("%H:%M:%S")
    user_message = '\n' + setCyan('Updated: \033[0;36;40m{}'.format(nowTxt))

    #command from received chat
    command_fromchat = recentMessage.text
    
    #name of the person that sent the chat
    name_commander = recentMessage.name
    fullname = name_commander.split()            
    
    #* the words from the most recent post as a list
    try:
        chatcommand = command_fromchat.split()
    except AttributeError:
        return

    
    # *censoring bad words
    if findBadWord(chatcommand):

        #* old guys don't get stopped
        if name_commander in bad_word_exemptions:
            return
        send_message('New guy {} no swearing'.format(fullname[0]))
        user_message = 'Swear word detection'
        update(user_message)

    keyword_fromchat_raw = chatcommand[0]
    
    try:
        action_fromchat_raw = chatcommand[1]

        #keyword not case sensitive
        keyword_fromchat = keyword_fromchat_raw.lower()
        action_fromchat = action_fromchat_raw.lower()

        nline = lines[1]
        jline = lines[0]
        message = nline.text
        
        #if the most recent chat invokes a command
        
        botname = self_name.lower().split()
        if keyword_fromchat == "${}bot".format(botname[0]):
            match action_fromchat:
                
                #echoing the last message sent
                case 'echo':
                    
                    if message[:9] == "${}bot".format(botname[0]):
                        pass
                    else:
                        user_message = '\nCommand {} invoked'.format(action_fromchat)
                        
                        send_message(message)
                        update(user_message)
                
                #telling the time
                case 'time':
                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    message = 'The time right now is {}'.format(timeTxt)
                    send_message(message)
                    update(user_message)

                #simply just saying hi
                case 'hi':
                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    message = 'Hi {} 😀! '.format(jline.name)
                    send_message(message)
                    update(user_message)

                #liking the most recent message
                case 'like':
                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    like_recent_message()
                    update(user_message)


                #* for web searching
                #google search
                case 'google'|'search':
                    # todo maybe add except case for not enough inputs
                    
                    search_array = chatcommand[2:]
                    if len(search_array) < 1:
                        return
                    
                    #the search to search
                    search = ' '.join(search_array)

                    #the url
                    url = websearch(action_fromchat,search)

                    #sending the message out to chat
                    message = "Here's what I found: {}".format(url)
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)

                #youtube search
                case 'youtube':
                    # todo maybe add except case for not enough inputs
                    
                    search_array = chatcommand[2:]
                    if len(search_array) < 1:
                        return
                    
                    search = ' '.join(search_array)
                    
                    #the url
                    url = websearch(action_fromchat,search)

                    message = "Here's what I found: {}".format(url)
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)
                
                #wiki search    
                case 'wiki':
                    # todo maybe add except case for not enough inputs
                    
                    search_array = chatcommand[2:]
                    if len(search_array) < 1:
                        return
                    
                    search = ' '.join(search_array)
                    
                    #the url
                    url = websearch(action_fromchat,search)

                    message = "Here's what I found: {}".format(url)
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)

                #thesaurus
                case 'thesaurus':
                    # todo maybe add except case for not enough inputs
                    
                    search_array = chatcommand[2:]
                    if len(search_array) < 1:
                        return
                    
                    search = ' '.join(search_array)
                    
                    #the url
                    url = websearch(action_fromchat,search)

                    message = "Here's what I found: {}".format(url)
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)
                
                #dictionary
                case 'dictionary':
                    search_array = chatcommand[2:]
                    if len(search_array) < 1:
                        return
                    
                    search = ' '.join(search_array)
                    
                    #the url
                    url = websearch(action_fromchat,search)

                    message = "Here's what I found: {}".format(url)
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)

                #* wordle !!!
                case 'wordle':
                    
                    global arr
                    global counter
                    global wordIdx
                    
                    #the words list
                    with open('words.txt', 'r') as f:
                        wordLines = f.readlines()
                        words = []
                        for line in wordLines: 
                            word = line.strip()
                            words.append(word)

                    #the word that comes after "wordle" is the guess
                    wordGuess = chatcommand[2]

                    #a function to reset the game
                    def resetGame():
                        wordIdx = randint(0,5757)
                        arr = [ 
                            "     ", 
                            "     ", 
                            "     ", 
                            "     ", 
                            "     ", 
                            "     ", 
                        ]
                        counter = 0
                        return arr,counter,wordIdx
                        
                    #testword CHEEK
                    theword = 'CHEEK'
                    theword = words[wordIdx]
                    theword = theword.upper()

                    #making the thing case-insensitive
                    wordGuess = wordGuess.upper()
                    if len(wordGuess) != 5:
                        send_message("Invalid word length!")
                        return
                    if wordGuess == 'DXDUI':
                        send_message(theword)
                        return
                    #checking for not-word inputs
                    if wordGuess.lower() not in words:
                        send_message("Invalid word input!")
                        return

                    # arr.append(wordGuess)
                    arr[counter] = wordGuess
                    
                    #* wordle
                    winner = wordle_run(arr,theword)

                    send_picture('result.PNG')
                    # send_message(theword)

                    #someone winning
                    if winner == True:
                        name_commander
                        send_message('{} Wins!'.format(fullname[0]))
                        arr, counter, wordIdx = resetGame()
                        return
                    
                    counter += 1

                    #losing
                    if counter == 6:
                        arr, counter, wordIdx = resetGame()
                        send_message('Everyone loses 😥. The word was {}.'.format(theword))
                        return
                    
                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)

                #approving and disapproving
                case 'disapprove':
                    message = "👎"
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)
                case 'approve':
                    message = "I approve 👍"
                    send_message(message)

                    user_message = '\nCommand {} invoked'.format(action_fromchat)
                    update(user_message)
                    

                #a command to deactivate this from chat, but it's not very graceful.
                case 'deactivate':
                    raise KeyboardInterrupt

                case _:
                    pass
    except IndexError:
        pass


def main():
    os.system('cls')
    
    #channel and group
    global channel
    global group_to_pick

    #!define any global arrays that the bot will use at the time of launching
    #* this specifically is for wordle
    global arr
    global counter
    global wordIdx
    arr = [ 
        "     ", 
        "     ", 
        "     ", 
        "     ", 
        "     ", 
        "     ", 
    ]
    counter = 0
    wordIdx = randint(0,5757)
    
    channel = channel_Menu()
    group_to_pick = channel.name

    send_message(f"{self_name.lower().split()[0]}bot Activated 🤡")

    try:
        update('\nEntered Channel: \033[1;32;40m{}\033[0;37;40m'.format(group_to_pick))
        
        #making the ui window
        root = Tk()
        root.title("Run Bot")
        root.geometry('220x80')
        root.resizable(0,0)
        myLabel = Label(root, text='Current Channel: {}'.format(group_to_pick), font=('Helvetica',10,'bold'))
        myLabel.pack()

        #function to quit the bot
        def quitter():
            send_message(f"{self_name.lower().split()[0]}bot Deactivated 😢")
            root.destroy()

        quitButton = Button(root, text = 'Quit Bot', command = quitter)
        quitButton.pack(pady=10)

        def ticker():
            run_bot()
            update(user_message)
            quitButton.after(1000, ticker)

        #calling the initial function
        ticker()          

        root.mainloop()

    #this isn't very good
    except KeyboardInterrupt:        
        return
        
if __name__  == '__main__':
    main()

