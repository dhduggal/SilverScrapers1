from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import time

area_list = []
zip_list = []

area_df = pd.DataFrame()
area_df = pd.read_csv('just_eat_data_zip_code_list.csv')

area_list = []
zip_list = []
for area_indiv, zip_indiv in zip(area_df['Area'], area_df['Postcode']):
    area_list.append(area_indiv)
    new_zip_indiv = zip_indiv.replace(" ", "%20")
    zip_list.append(new_zip_indiv)

links = []
base_url = "https://www.just-eat.co.uk/area/"
for l in zip_list:
    url = base_url + l
    links.append(url)

print(links)


driver = webdriver.Firefox()
zip_list = []
names_lists = []
categories_list_list = []
rating_ppl_list = []
rating_list = []
delivery_time_list = []
promoted_list = []
discount_list = []
location_list = []
del_cost_list = []
min_cost_list = []
link_count = 0
count = 0
print(len(links))

start = time.time()
for j in links:
    link_count += 1
    print(link_count, end="...\n")
    driver.get(j)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    all_rest = soup.findAll("section", {"data-test-id": "restaurant"})

    for i in all_rest:
        count += 1
        zip_list.append(j)
        name = i.find("h3",{"class":"c-listing-item-title"}).get_text().strip()
        names_lists.append(name)
        categories_section= i.find("p",{"itemprop":"servesCuisine"})
        category_list = []
        if categories_section is not None:
            categories = i.find("p",{"itemprop":"servesCuisine"}).get_text().split('\n')
            for cat in categories:
                if cat != "":
                    category_list.append(cat.strip())
        else:
            categories = None
            category_list = []
        categories_list_list.append(category_list)
        rating_ppl = i.find("strong",{"class": "c-listing-item-ratingText"})
        if rating_ppl is not None:
            rating_ppl_final = rating_ppl.get_text().strip()
        else:
            rating_ppl_final = None
        rating_ppl_list.append(rating_ppl_final)

        rating = i.find("span", {"data-test-id": "review_avg"})
        if rating is not None:
            rating_final = rating.get_text().strip()
        else:
            rating_final = None
        rating_list.append(rating_final)

        # shows only if the restaurant is currently closed
        check_delivery_time = i.find("p", {"data-test-id": "restaurant_delivery_time"})
        if check_delivery_time is not None:
            delivery_time = check_delivery_time.get_text().strip()
        else:
            delivery_time = None
        delivery_time_list.append(delivery_time)

        check_promoted = i.find("span", {"data-test-id": "restaurant-sponsored"})
        if check_promoted is not None:
            promoted = "Yes"
        else:
            promoted = "No"
        promoted_list.append(promoted)

        check_discount = i.find("p", {"data-test-id": "restaurant-discounts"})
        if check_discount is not None:
            discount = check_discount.get_text().strip()
        else:
            discount = None
        discount_list.append(discount)

        check_location = i.find("p", {"data-test-id": "location"})
        if check_location is not None:
            location = check_location.get_text().strip()
        else:
            location = None
        location_list.append(location)

        check_cost_delivery = i.find("p", {"data-test-id": "restaurant_delivery_details"})
        if check_cost_delivery is not None:
            split_del_cost = check_cost_delivery.get_text().split('\n')
            del_cost = split_del_cost[1].strip()
            min_cost = split_del_cost[3].strip()
        else:
            del_cost = None
            min_cost = None
        del_cost_list.append(del_cost)
        min_cost_list.append(min_cost)
end = time.time()
print("Time taken in seconds =", end=" ")
print(end-start)
print(count)

data = d = {'zip-code': zip_list, 'name': names_lists, 'categories':categories_list_list, 'ratings': rating_list,
            'no. people rated': rating_ppl_list, 'delivery_time':delivery_time_list, 'promoted': promoted_list,
            'discount':discount_list,'location':location_list,'del_cost': del_cost_list, 'min_cost': min_cost_list}
df = pd.DataFrame(data=d)
df.to_csv("just_eat_data_full_unformated.csv")




