#Pybuster V0.0.0

#Please view README for more information


import socket
import datetime
import requests
import platform

#State based application

###### Initialising Variables ######

version = "1.0.1"
states = ["input", "searching", "results", "end"]
targetUrl = ""
targetPort = ""
currentState= "input"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wordlist = ""
extensionlist = ""
connected = False
url_count = 0
finished_words = []
finished_urls = []
found_urls = []
found_codes = []
running = True
log_count = 0
system = ""
slash = ""


###### Functions ######

#Crafts the url needed and sends the GET request to server
def bustTarget(url_list):
    for url in url_list:
        r = requests.get(url)
        if r.status_code !=404:
            found_urls.append(url)
            found_codes.append(r.status_code)




#Iterates through both the word list and extension list, appending the words together and crafting the URL

def iterateLists(word, ext, url):
    ext.append("")
    for line1 in ext:
        for line2 in word:
            x = line1
            y = line2
            z = y.strip()+x.strip()
            finished_words.append(z)

    for i in finished_words:
        finished_urls.append("http://" + url + ":" + str(targetPort) + "/" + i)


##Initialising what system the user is on and assinging correct forward/backslash for that OS
system = platform.system()
if system == "Windows":
        print("we got here")
        slash = '\\'
elif system == "Linux":
        slash = '/'
else:
        slash = "error on filesystem type"


###### Logic ######




## -- Input stage -- ##

#While in user input stage, handle all input and get everything initiated
while running:

    while currentState == states[0]:
##Detects users OS to ensure correct res loaded
        logo = open("lib" + slash + "p_res" + slash + "pybuster_logo.txt")
        for line in logo.readlines():
            line.split()
            print(line)
        print("-----------------Welcome to PyBuster Version " + version + "------------------")
        print("-------------------------[Type Exit to leave]---------------------------------")
        print("-----------------[Read the README.txt file for more help]---------------------")
#This if statements relates to logs. If a log has been made, it shows it here because if it shows it at the end
#the confirmation for the log dissappears into the CLI
        if(log_count > 0):
            print("Log stored as " + logname + " in " + slash + "PyBuster" + slash + "logs")
        while connected == False:
            print("Enter target URL: ")
            targetUrl = str(input())
            if targetUrl.capitalize() != "Exit":
                print("Enter target port for " + targetUrl + ": ")
                targetPort = int(input())
#Statically set target port for testing purposes, speeds up input process
                #targetPort = 8000
                try:
                    s.connect((targetUrl, targetPort))
                    connected = True
                    print("Connection established...")
                except:
#Provides some detail on format for the user to follow if they're having troubles
                        print("Unable to connect to Host at " + targetUrl + ":" + str(targetPort))
                        print("Esnure URL format is >somewhere.com and is NOT >http//:somewhere.com")
                        print("Common http ports include 80, 8000, 8080")

#Making sure the user enters valid paths
        while wordlist == "" and currentState != states[3]:
            print("Enter wordlist path: ")
            try:
                wordlist = open(input())
# Statically set wordlist for testing purposes, speeds up input process
                #wordlist = open("lib\lists\words.txt")
                wordlist_raw = wordlist.readlines()
                print("Loaded wordlist: " + wordlist.name)
            except:
                print("Incorrect file path, try again")


        while extensionlist == "" and currentState != states[3]:
            print("Enter extentionlist path: ")
            try:
                extensionlist = open(input())
# Statically set extensionlist for testing purposes, speeds up input process
                #extensionlist = open("lib\lists\extensions.txt")
                extensionlist_raw = extensionlist.readlines()
                print("Loaded extension list: " + extensionlist.name)
            except:
                print("Incorrect file path, try again")
        if currentState != states[3]:
            currentState = states[1]

## -- Searching stage -- ##
    while currentState == states[1]:
#Bannner for PyBuster outlining key details

        print("--------\nPyBuster\n--------")
        start_time = datetime.datetime.now()
        print("Start time: " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("URL: " + targetUrl)
        print("Wordlist: " + wordlist.name)
        print("Extensionlist: " + extensionlist.name + "\n--------")
        print("Words checking: " + str(len(wordlist_raw)) + "\nExtensions checking: " + str(len(extensionlist_raw) + 1)
              + "\nTotal URLs checking: " +str(len(wordlist_raw) * (len(extensionlist_raw) + 1)))
        print("Busting... Please wait.")
#Merging the 2 lists
        iterateLists(wordlist_raw, extensionlist_raw, targetUrl)

#Using the the merged lists to craft the url and then send the requests
        bustTarget(finished_urls)
        currentState = states[2]

## -- Results stage -- ##

#Display all found URLs
    while currentState == states[2]:
        print("          |          ")
        for found in found_urls:
            count = 0
            print("     Found url: " + found + " - Status code: " + str(found_codes[count]))
            count = count+1
        print("          |          ")
        end_time = datetime.datetime.now()
        print("-{STAT} End time: " + end_time.strftime(("%Y-%m-%d %H:%M:%S")))
        time_taken = end_time - start_time
        print("-{STAT} Time taken: " + str(time_taken))
        print("-{STAT} Total successful URLs: "  + str(len(found_urls)) + "/" + str(len(wordlist_raw) *
                                                                                  len(extensionlist_raw)))

#Clean up by closing all open connections to external sources.
        s.close()
        wordlist.close()
        extensionlist.close()
        print("Connection closed")

#Test if user wants to do another PyBust, store the log or exit
        again = input("[P] to PyBust new target - [L] to store as log - [E] to exit").capitalize()
        if again == "P":
            connected = False;
            currentState = states[0]
            break;
        elif again == "L":
#Setting appropriate name and storing everything that was outputted to a .txt file in Pybuster/logs
            logname = "PB log - " + start_time.strftime("%Y_%m_%d %H_%M_%S")
            log = open("logs/" + logname + ".txt", 'w')
            log.write("--------\nPyBuster\n--------")
            log.write("\nStart time: " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
            log.write("\nURL: " + targetUrl)
            log.write("\nWordlist: " + wordlist.name)
            log.write("\nExtensionlist: " + extensionlist.name + "\n--------")
            log.write("\nWords checking: " + str(len(wordlist_raw)) + "\nExtensions checking: " + str(len(extensionlist_raw))
                  + "\nTotal URLs checking: " + str(len(wordlist_raw) * len(extensionlist_raw)))
            log.write("\nBusting... Please wait.")
            log.write("\n          |          ")
            for found in found_urls:
                count = 0
                log.write("\n     Found url: " + found + " - Status code: " + str(found_codes[count]))
                count = count + 1
            log.write("\n          |          ")
            log.write("\n-{STAT} End time: " + end_time.strftime(("%Y-%m-%d %H:%M:%S")))
            log.write("\n-{STAT} Time taken: " + str(time_taken))
            log.write("\n-{STAT} Total successful URLs: " + str(len(found_urls)) + "/" + str(len(wordlist_raw) *
                                                                                       len(extensionlist_raw)))
            log.close()
            log_count = log_count + 1
            connected = False;
            currentState = states[0]
        elif again == "E":
            finish = False;
            currentState = states[3]
        else:
            print("Incorrect input")
#Exit
    if(currentState == states[3]):
        print("Goodbye")
        running = False;