#Pybuster V0.0.0

#Please view README for more information


import socket
import datetime
import requests

#State based application

###### Initialising Variables ######

states = ["input", "searching", "results", "end"]
targetUrl = ""
targetPort = ""
currentState= "input"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wordlist = ""
extensionlist = ""
connected = False;
url_count = 0
finished_words = []
finished_urls = []
found_urls = []
found_codes = []
running = True;



###### Functions ######

#Crafts the url needed and sends the GET request to server
def bustTarget(url_list):
    for url in url_list:
        r = requests.get(url)
#------------------------IMPORTANT: Take 404 out before actual use, testing purposes only--------------------------#
        if r.status_code == 200 or r.status_code == 403 or r.status_code == 404:
            found_urls.append(url)
            found_codes.append(r.status_code)




#Iterates through both the word list and extension list, appending the words together and crafting the URL

def iterateLists(word, ext, url):
    for line1 in ext:
        for line2 in word:
            x = line1
            y = line2
            z = y.strip()+x.strip()
            finished_words.append(z)
    for i in finished_words:
        finished_urls.append("http://" + url + ":" + str(targetPort) + "/" + i)



###### Logic ######




## -- Input stage -- ##

#While in user input stage, handle all input and get everything initiated
while running:

    while currentState == states[0]:
        logo = open("lib\p_res\pybuster_logo.txt")
        for line in logo.readlines():
            line.split()
            print(line)
        print("------------------Welcome to PyBuster Version 1.0.0------------------")
        print("[Type Exit at any time to leave]")

        while connected == False:
            print("Enter URL: ")
            targetUrl = input()
            print(targetUrl.capitalize())
            if targetUrl.capitalize() == "Exit":
                currentState = states[3]
                connected = True

            #print("Enter port: ")
            #targetPort = int(input())
            targetPort = 8000
            try:
                s.connect((targetUrl, targetPort))
                connected = True
                print("Connection established...")
            except:
                print("Unable to connect to Host at " + targetUrl + ":" + str(targetPort))


    #Making sure the user enters valid paths

        while wordlist == "" and currentState != states[3]:
            print("Enter wordlist path: ")
            try:
                #wordlist = open(input())
                wordlist = open("lib\lists\words.txt")
                wordlist_raw = wordlist.readlines()
                print("Loaded wordlist: " + wordlist.name)
            except:
                print("Incorrect file path, try again")


        while extensionlist == "" and currentState != states[3]:
            print("Enter extentionlist path: ")
            try:
                #extensionlist = open(input())
                extensionlist = open("lib\lists\extensions.txt")
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
        print("Words checking: " + str(len(wordlist_raw)) + " Extensions checking: " + str(len(extensionlist_raw))
              + " Total URLs checking: " +str(len(wordlist_raw) * len(extensionlist_raw)))
    #Merging the 2 lists
        iterateLists(wordlist_raw, extensionlist_raw, targetUrl)

    #Using the the merged lists to craft the url and then send the requests
        bustTarget(finished_urls)
        currentState = states[2]


    ## -- Results stage -- ##

    #Display all found URLs
    while currentState == states[2]:
        for found in found_urls:
            count = 0
            print("     Found url: " + found + " - Status code: " + str(found_codes[count]))
            count = count+1
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

    #Test if user wants to do another PyBust
        again = input("Bust new host? [y/n]").capitalize()
        if again == "Y":
            connected = False;
            currentState = states[0]
            break;
        elif again == "N":
            finish = False;
            currentState = states[3]
            break;
        else:
            print("Incorrect input")
    #Exit
    if(currentState == states[3]):
        print("Goodbye")
        running = False;
