from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class RealEstateAgent:
    name = ''
    number = ''
    def __init__(self, _name, _number) :
        self.name = _name
        self.number = _number

    def PrintMe(self) :
        print(self.name + " " + self.number + '\n')
    
    def WriteText(self) : 
        return self.name + " " + self.number + '\n'

class RLAManager:
    agents = []

    def __init__(self) :
        #Do Nothing
        agents = []

    def PrintAgents(self) :
        for currentA in self.agents :
            currentA.PrintMe()
    
    def WriteAgents(self, file_path) :
        file = open(file_path, "w")
        for currentA in self.agents :
            file.write(currentA.WriteText())
        file.close()

    
PAGES_TO_SCRAPE = 80

def test_html_save():

    agentManager = RLAManager()
    myNumb = 0
    while(myNumb < PAGES_TO_SCRAPE) :
        playlist_url = 'https://www.realtor.com/realestateagents/knoxville_tn/pg-' + str(myNumb + 1)
        browser = webdriver.Chrome()
        browser.get(playlist_url)
        time.sleep(4) #Waits for 4 secs until the page loads
        html_content = browser.page_source  # Getting the html from the webpage
        browser.close()
        soup = BeautifulSoup(html_content, 'html.parser') # creates a beautiful soup object 'soup'.

        html_save_path = "C:\\bs4_html.txt"

        with open(html_save_path, 'wt', encoding='utf-8') as html_file:
            for line in soup.prettify():
                html_file.write(line)

        names = soup.find_all("div", class_="jsx-2987058905 agent-name text-bold")
        numbers = soup.find_all("div", class_="jsx-2987058905 agent-phone hidden-xs hidden-xxs")


        

        # FIND THE CARD
        agentCards = soup.find_all('div', {'class': 'jsx-2987058905 agent-list-card-title col-lg-3 col-sm-4 col-xxs-12 mobile-only clearfix'})
        
        for element in agentCards :
            # GET THE DIVS WITH NAME
            _s_name   = element.findChildren("div" , {"class": 'jsx-2987058905 agent-name text-bold'}, recursive=True)[0].text
            # GET THE DIVS WITH NUMBER
            numberElements = element.findChildren("div" , {"class": 'jsx-2987058905 agent-phone hidden-xs hidden-xxs'}, recursive=True)
            _s_number = ''
            if len(numberElements) > 0 :
                _s_number = numberElements[0].text
            else :
                _s_number = ''
            
            # ADD TO LIST OF AGENTS
            agentManager.agents.append(RealEstateAgent(_s_name, _s_number))
        myNumb += 1
    # PRINT AGENTS
    #agentManager.PrintAgents()
    agentManager.WriteAgents("example.txt")
test_html_save()

