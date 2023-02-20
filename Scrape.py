# AUTHOR       : ANDREW HUDSON
# DESCRIPTION  : SIMPLE WEB SCRAPER EXAMPLE I USED TO SCRAPE REALATORS INFORMATION FOR MY MOM, IT SIMPLY PRINTS THEIR NAMES AND THEIR NUMBERS INTO A TEXT FILE IN THE SAME DIRECTORY
# INSTRUCTIONS : OPEN WITH VISUAL STUDIO CODE CHANGE THE PATH VARITABLES TO LIKING (THEY ARE FOUND STARTING ON LINE 53) THEN DO THE COMMAND "Python Scrape.py" AND BAM! REALTORS IN KNOXVILLE TN TO HARRASS FOR WHATEVER REASON U MAY DESIRE

from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class RealEstateAgent:
    name = ''       # The Real Estate Agent's Name
    number = ''     # The Real Estate Agent's Phone Number

    # Name        : __init__(_name, _number)
    # Description : Initilizes the object with the given name (_name) and phone number (_number)
    def __init__(self, _name, _number) :
        self.name = _name
        self.number = _number

    # Name        : PrintMe()
    # Description : Prints the objects name and number to the console
    def PrintMe(self) :
        print(self.name + " " + self.number + '\n')
    
    # Name        : 
    # Description : 
    def WriteText(self) : 
        return self.name + " " + self.number + '\n'

class RLAManager:
    agents = []

    # Name        : __init__() (CONSTRUCTOR)
    # Description : Initilizes the Object
    def __init__(self) :
        self.agents = []

    # Name        : PrintAgents()
    # Description : Prints all the Agets to the console...
    def PrintAgents(self) :
        for currentA in self.agents :
            currentA.PrintMe()
    
    # Name        : WriteAgents(file_path)
    # Description : Writes agents names and numbers to the given file path
    def WriteAgents(self, file_path) :
        file = open(file_path, "w")
        for currentA in self.agents :
            file.write(currentA.WriteText())
        file.close()


PAGES_TO_SCRAPE              = 2                                                                                                                  # NUMBER OF PAGES YOU WOULD LIKE TO SCRAPE
FILE_NAME                    = "Solicitation_Victims.txt"                                                                                         # FILE NAME WHERE ALL THE INFO WILL BE STORED
AGENT_CARD_DIV_CLASS         = 'jsx-2987058905 agent-list-card-title col-lg-3 col-sm-4 col-xxs-12 mobile-only clearfix'                           # THE DIVS CLASS THAT HOLDS THE INFO WE WANT
AGENT_NAME_DIV_CLASS         = 'jsx-2987058905 agent-name text-bold'                                                                              # THE DIVS CLASS THAT HOLDS THE NAME OF AGENT
AGENT_PHONE_NUMBER_DIV_CLASS = 'jsx-2987058905 agent-phone hidden-xs hidden-xxs'                                                                  # THE DIVS CLASS THAT HOLDS THE PHONE NUMBER OF AGENT
SAVE_HTML_PAGES              = False                                                                                                              # BOOL REPRESENTING IF YOU WOULD LIKE TO SAVE THE HTML (NEEDS TO BE RAN AS ADMIN)
HTML_SAVE_PATH               = "C:\\HTML\Page"                                                                                                    # THE FILE PATH WHERE THE HTML WILL BE STORED

def test_html_save():

    agentManager = RLAManager()                                                                                                                   # Setup Real Estate Agent Manager
                                 
    currentPageNumber = 0                                                                                                                         # Will be used for iterating over the pages
    while(currentPageNumber < PAGES_TO_SCRAPE) :                                             
        url = 'https://www.realtor.com/realestateagents/knoxville_tn/pg-' + str(currentPageNumber + 1)                                            # Get the URL Currently Needed (VERY SPECIFIC URL)
                                 
        browser = webdriver.Chrome()                                                                                                              # Set my Browser to use Chrome
        browser.get(url)                                                                                                                          # Open the webpage in Chrome
                                 
        time.sleep(4)                                                                                                                             # Waits for 4 secs until the page loads
                                 
        html_content = browser.page_source                                                                                                        # Getting the html from the webpage
        browser.close()                                                                                                                           # Close Browser after getting Data
                                 
        soup = BeautifulSoup(html_content, 'html.parser')                                                                                         # creates a beautiful soup object 'soup'.

        if SAVE_HTML_PAGES == True :                                                                                                              # IF SAVE_HTML_PAGES == True
            with open(HTML_SAVE_PATH + " ("+ str(currentPageNumber) + ")" + ".txt", 'wt', encoding='utf-8') as html_file:                                                                            # Open File to save html 
                 for line in soup.prettify():                                                                                                     # For each line in the html
                     html_file.write(line)                                                                                                        # Write it to the file


        

        # FIND THE CARD
        agentCards = soup.find_all('div', {'class': AGENT_CARD_DIV_CLASS})                                                                        # Find all the agent Cards
        
        for element in agentCards :
            # GET THE DIVS WITH NAME
            _s_name   = element.findChildren("div" , {"class": AGENT_NAME_DIV_CLASS}, recursive=True)[0].text
            # GET THE DIVS WITH NUMBER
            numberElements = element.findChildren("div" , {"class": AGENT_PHONE_NUMBER_DIV_CLASS}, recursive=True)
            _s_number = ''
            if len(numberElements) > 0 :                                                                                                          # CHECK IF CONTAINS A NUMBER
                _s_number = numberElements[0].text                                                                                                # SET temp string used for phone number
            else :
                _s_number = 'N/A'                                                                                                                 # If no number found make the document say N/A
            
            # ADD TO LIST OF AGENTS
            agentManager.agents.append(RealEstateAgent(_s_name, _s_number))                                                                       # Add the Agent to the Agent Manager

        # INCREMENT PAGE NUMBER
        currentPageNumber += 1                                                                                                                    # Increment the page Number
    # WRITE AGENTS TO FILE
    agentManager.WriteAgents(FILE_NAME)                                                                                                           # When you have all the data write it to a file
test_html_save()

