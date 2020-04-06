from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from selenium.webdriver.common.keys import Keys

area_df = pd.DataFrame()
area_df = pd.read_csv("just_eat_data_zip_code_list.csv")

area_list = []
zip_list = []
base_url = "https://deliveroo.co.uk/"

links = []

for area_indiv, zip_indiv in zip(area_df['Area'], area_df['Postcode']):
    lower_area_indiv = area_indiv.lower()
    area_list.append(lower_area_indiv)
    new_zip_indiv =  zip_indiv.replace(" ", "+")
    zip_list.append(new_zip_indiv)

driver = webdriver.Firefox()

start = time.time()
base_url_1 = "https://deliveroo.co.uk/restaurants/london/beckenham?postcode="
base_url_2 = "&sort=distance"

for url in zip_list:
    new_url = base_url_1 + url + base_url_2
    links.append(new_url)

name_list = []
delivery_time_list = []
rating_list = []
categories_list = []
delivery_cost_list = []
delivery_distance_list = []
promo_list = []
delivering_bool_list = []
final_zip_list = []
final_url_list = []


iteration = 0
outer_count = 0
for j, zip_code_new in zip(links,zip_list):

    iteration += 1
    driver.get(j)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    check_in_location = soup.find("h3",{"class": "ccl-2a4b5924e2237093 ccl-21bead492ce4ada2 ccl-99c566dc40a8a156 ccl-f7d830a9c75473b8"})

    if check_in_location is not None:
        print("Not in Location")
        print(j)
        name_list.append(None)
        delivery_time_list.append(None)
        rating_list.append(None)
        categories_list.append(None)
        delivery_cost_list.append(None)
        delivery_distance_list.append(None)
        promo_list.append(None)
        delivering_bool_list.append(False)
        final_zip_list.append(zip_code_new.replace("+", " "))
        final_url_list.append(j)
        print("scraped from page", 0)
        print(iteration, end="...")
        outer_count = outer_count + 0

    else:
        print("In Location")
        print("https://deliveroo.co.uk/restaurants/london/putney?postcode=SW151RT&sort=distance")
        jsons = soup.findAll("script", {"id": "__NEXT_DATA__"})
        lol = json.loads(jsons[0].get_text())
        blocks = lol['props']['initialState']['home']['feed']['results']['data'][0]['blocks']
        inner_count = 0
        for i in blocks:
            inner_count = inner_count+1
            content_description = i['contentDescription']
            content_list = content_description.split(". ")
            name = None
            delivery_time = None
            rating = None
            categories = None
            for c in content_list:
                if c[0:3] == "Res":
                    name = c
                elif c[0:3] == "Del":
                    if c == "Delivers at " or c == "Delivers at .":
                        delivery_time = None
                    else:
                        delivery_time = c
                elif c[0:3] == "Rat":
                    rating = c
                elif c[0:3] == "Ser":
                    categories = c
            name_list.append(name)
            delivery_time_list.append(delivery_time)
            rating_list.append(rating)
            categories_list.append(categories)

            delivery_distance = None
            delivery_cost = None
            if i['uiContent']['default']['uiLines'][2]:
                delivery_details = i['uiContent']['default']['uiLines'][2]
                if delivery_details['uiSpans']:
                    delivery_details_spans = delivery_details['uiSpans']
                    for dets in delivery_details_spans:
                        if 'text' in dets:
                            if dets['text'] != "·":
                                if "delivery" in dets['text']:
                                    delivery_cost = dets['text']
                                elif "miles" in dets['text']:
                                    delivery_distance = dets['text']
            delivery_distance_list.append(delivery_distance)
            delivery_cost_list.append(delivery_cost)

            promo_info = None
            if len(i['uiContent']['default']['uiLines']) >= 4 and i['uiContent']['default']['uiLines'][3]:
                promo_details = i['uiContent']['default']['uiLines'][3]
                if promo_details['uiSpans']:
                    promo_details_spans = promo_details['uiSpans']
                    for prom in promo_details_spans:
                        if 'text' in prom:
                            promo_info = prom['text']
            promo_list.append(promo_info)
            final_zip_list.append(zip_code_new.replace("+", " "))
            final_url_list.append(j)
            delivering_bool_list.append(True)
        print("scraped from page", inner_count)
        print(iteration, end="...\n")
        outer_count = outer_count + inner_count

end = time.time()
print(end - start)
print(outer_count)
data = d = {'zip_codes': final_zip_list, 'urls': final_url_list, 'delivering':delivering_bool_list,
            'name': name_list, 'categories':categories_list, 'ratings': rating_list,
            'delivery_time': delivery_time_list, 'promos': promo_list, 'del_cost': delivery_cost_list,
            'del_dist': delivery_distance_list}

df = pd.DataFrame(data=d)
df.to_csv("deliveroo_data_full_unformated.csv")