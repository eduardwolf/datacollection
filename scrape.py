import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

all_listings = set()
yit_link = 'https://www.yit.sk/predaj-bytov/bratislava?tab=apartments&sort=ReservationStatusIndex&order=asc'
slnecnice_link = 'https://www.slnecnice.sk/byvanie?status[]=P'


# function to scrape all apartment listings on the yit website
def scrape_yit(link, limit):
    driver = webdriver.Chrome()
    counter = 1
    next_exists = True
    while next_exists and counter <= limit:  # this loop keeps going until there's no new link, limit for faster testing
        print("currently on yit page" + str(counter))
        driver.get(link + "&page=" + str(counter))  # navigate the driver to the desired link, paginated by the counter
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # parse HTML

        for article in soup.findAll('article'):  # iterate through listings

            class Listing:
                listing_id = article.find('h3').text.split()[0]
                status = article.find("span", class_="status").text
                term = article.find("span", class_="project-status").text

                dd_list = article.findAll("dd")  # all other necessary information is in the dd elements
                rooms = dd_list[0].text
                interior = dd_list[1].text
                # exterior is calculated as total - interior
                exterior = str(round(float(dd_list[2].text.split()[0]) - float(dd_list[1].text.split()[0]), 2)) + " m²"
                price = dd_list[3].text
                floor = dd_list[4].text

            all_listings.add(Listing())

        if soup.find("a", class_="paging__button--next"):  # finds whether there is a next page or if it's the end
            next_exists = True
            counter += 1
        else:
            next_exists = False


# function to scrape all apartment listings on the slnecnice website
def scrape_slnecnice(link, limit):
    driver = webdriver.Chrome()
    driver.get(link)
    counter = 1
    next_exists = True

    while next_exists and counter <= limit:  # this loop keeps going until there's no new link, limit for faster testing
        print("currently on slncecnice page" + str(counter))
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # parse HTML
        for row in soup.findAll('tr')[2:]:  # iterate through listings, first 2 rows removed - undesired data
            td_list = row.findAll("td")  # find td elements in current row, those contain the desired data

            class Listing:
                listing_id = td_list[1].text
                status = td_list[9].text
                term = td_list[8].text
                rooms = td_list[3].text
                interior = td_list[4].text
                exterior = td_list[5].text
                price = td_list[7].text
                floor = td_list[6].text

            all_listings.add(Listing())

        time.sleep(1)
        try:  # finds whether there is a next page or if it's the end
            next_click = driver.find_element(By.XPATH, "//a[@aria-label='Nasledujúca stránka']")
            driver.execute_script("arguments[0].click();", next_click)
            counter += 1
        except:
            next_exists = False


scrape_yit(yit_link, 3)  # second parameter limits how many pages it cycles through, 100 should be enough for all
scrape_slnecnice(slnecnice_link, 3)

# create/replace current db
connection = sqlite3.connect('database.db')
connection.execute('''DROP TABLE IF EXISTS listings''')
connection.execute('''CREATE TABLE listings
             (listing_id TEXT PRIMARY KEY, status TEXT, term TEXT, rooms TEXT, interior TEXT, exterior TEXT, price TEXT, floor TEXT)''')

# insert each listing
for listing in all_listings:
    connection.execute("INSERT INTO listings (listing_id, status, term, rooms, interior, exterior, price, floor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (listing.listing_id, listing.status, listing.term, listing.rooms, listing.interior, listing.exterior, listing.price, listing.floor))

connection.commit()
connection.close()
