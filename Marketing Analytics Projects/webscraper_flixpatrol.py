#!/usr/bin/env python
# coding: utf-8

# # Web scraper | FlixPatrol
# Import packages
from pip._vendor import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

#debug = {'verbose': sys.stderr}
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'}  

# Creating urls to loop thru on Flixpatrol

# creating a function to collect all page urls of competitors (Hulu, HBO Max & Disney+)
base_url_comp = "https://flixpatrol.com/top10/"

# Now create the function
def generate_page_urls_comp(base_url_comp, platform):
    page_urls_comp = []
    
    # first 10 urls
    for i in range(1, 10):
        full_url_comp = base_url_comp + str(platform) + "/united-states/2022-00" + str(i)
        page_urls_comp.append(full_url_comp)
    # remaining urls 
    for i in range(10, 53):
        full_url_comp = base_url_comp + str(platform) + "/united-states/2022-0" + str(i)
        page_urls_comp.append(full_url_comp)
    
    return page_urls_comp

# creating a function to collect all page URLs of Amazon (Amazon Video & Amazon Prime)
base_url_amazon = "https://flixpatrol.com/top10/"

# Now create the function
def generate_page_urls_amazon(base_url_amazon):
    page_urls_amazon = []
    
    # first 10 urls Amazon Video
    for i in range(1, 10):
        full_url_amazon = base_url_amazon + "amazon" + "/united-states/2022-00" + str(i)
        page_urls_amazon.append(full_url_amazon)
    # remaining 10 urls Amazon Video
    for i in range(10, 20):
        full_url_amazon = base_url_amazon + "amazon" + "/united-states/2022-0" + str(i)
        page_urls_amazon.append(full_url_amazon)
    # remaining Amazon Prime
    for i in range(20, 53):
        full_url_amazon = base_url_amazon + "amazon-prime" + "/united-states/2022-0" + str(i)
        page_urls_amazon.append(full_url_amazon)
    
    return page_urls_amazon

# creating a function to collect all page URLs of Netflix
base_url_netflix = "https://flixpatrol.com/top10/netflix/united-states/2022-"

# Now create the function
def generate_page_urls_po_netflix(base_url_po):
    page_urls_netflix = []
    
    for i in range(1, 10):
        full_url_netflix = base_url_netflix + "00" + str(i) + "/official/#netflix-1"
        page_urls_netflix.append(full_url_netflix)
    for i in range(10, 53):
        full_url_netflix = base_url_netflix + "0" + str(i) + "/official/#netflix-1"
        page_urls_netflix.append(full_url_netflix)
    
    return page_urls_netflix

# Creating one list with all urls

# creating list with all urls
page_urls = generate_page_urls_comp("https://flixpatrol.com/top10/", "hulu") + generate_page_urls_comp("https://flixpatrol.com/top10/", "hbo") + generate_page_urls_comp("https://flixpatrol.com/top10/", "disney") + generate_page_urls_amazon("https://flixpatrol.com/top10/") + generate_page_urls_po_netflix("https://flixpatrol.com/top10/")
test = page_urls[:2]
test
# Loop thru all gathered pages on Flixpatrol
def get_rank_info(rank_urls):
    rank_pages = []
    
    # loop thru url in page_urls
    for url in test: 
        res = requests.get(url, headers = user_agent)
        sleep(5)
        soup = BeautifulSoup(res.text, "html.parser")
        # find chart block
        headers = soup.findAll("div", class_="content mb-14")
        
        for header in headers:
            # movie/tv-show header with: type, week number and platform
            block_header = header.find("h2", class_="mb-3").text
            # rank information
            rank_info = header.find_all("tr", class_="table-group")
            
            # split the header to get week number, type, and platform
            # remove useless header
            if "by day" in block_header:
                continue
            else:
                header_parts = block_header.split(" on ")
                #type: movie/TV-show
                Type = header_parts[0].replace("TOP","").strip()
                #platform
                platform = header_parts[1]
                week = header_parts[2].split()
                # weeknumber
                week_num = week[1]

            for rank in rank_info:   
                #title link
                title_link = rank.find("a").attrs["href"]
                #title name
                title_name = rank.findAll('div')[2].text.strip()
                #exlusive
                exclusive = rank.findAll("span", class_="inline-block align-baseline w-3 h-3")
                #current rank
                ranking = rank.findAll('td')[0].text
                ranking = ranking.replace(".", "")
                #cumulative rank
                cumulative_rank = rank.findAll('td')[2].text
                
                # append all data to list
                rank_pages.append({"title link": "flixpatrol.com" + title_link,
                                        "rank": ranking,
                                        "title name": title_name,
                                        "cumulative_rank": cumulative_rank,
                                        "exclusive": exclusive,
                                        "Type": Type,
                                        "platform": platform,
                                        "week_num": week_num})
                             
   
    return rank_pages

# apply above created function to the gathered url list for all platforms and store it into a new variable
rank_information = get_rank_info(test)

# write datafile into a csv file
with open("rank_information_comp_vs10.csv", "w", encoding = 'utf-8', newline='') as csv_file: 
    writer = csv.writer(csv_file, delimiter = ";")
    writer.writerow(["title link", "rank", "title name", "cumulative_rank", "Type", "platform", "week_num"])
    for rank in rank_information: 
        writer.writerow([rank['title link'], rank['rank'], rank['title name'], rank['cumulative_rank'], rank['Type'], rank['platform'], rank['week_num']])
print('done!')

# write title names to a list to use for the API
titles = []
for item in rank_information:
    titles.append(item["title name"])
titles
