from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def test_html_save():

    file = open("example.txt", "w")

    pagesToScrape = 25

    myNumb = 0
    while(myNumb < pagesToScrape) :
        playlist_url = 'https://www.realtor.com/realestateagents/knoxville_tn/pg-' + str(myNumb + 1)
        browser = webdriver.Chrome()
        browser.get(playlist_url)
        time.sleep(4) #Waits for 4 secs until the page loads
        html_content = browser.page_source  # Getting the html from the webpage
        browser.close()
        soup = BeautifulSoup(html_content, 'html.parser') # creates a beautiful soup object 'soup'.

        html_save_path = "D:\\bs4_html.txt"

        with open(html_save_path, 'wt', encoding='utf-8') as html_file:
            for line in soup.prettify():
                html_file.write(line)

        names = soup.find_all("div", class_="jsx-2987058905 agent-name text-bold")
        numbers = soup.find_all("div", class_="jsx-2987058905 agent-phone hidden-xs hidden-xxs")


        namesCount = 0
        numberCount = 0
        

        name = ''
        for element in names:
            if(element.text != name):
                    if(namesCount > numbers.__len__() - 2) :
                        file.write("NAME : " + element.text + " : " + "NO NUMBER : " + '\n')
                        
                    else :
                        file.write("NAME : " + element.text + " : " + "NUMBER : " + numbers[namesCount].text + '\n')
                        print(namesCount)
            name = element.text
            namesCount += 1

        myNumb += 1
    file.close()
test_html_save()

