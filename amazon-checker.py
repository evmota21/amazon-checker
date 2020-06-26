import requests
import re
from bs4 import BeautifulSoup


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


itemKeyword = input("Type item to find in stock: ")
itemToFindURL = itemKeyword.replace(' ', '+')
itemToFind = itemKeyword

URL = 'https://www.amazon.com.mx/s?k=' + itemToFindURL + '&__mk_es_MX=ÅMÅŽÕÑ&ref=nb_sb_noss_1'

print("GET URL Request: ", bcolors.WARNING + URL + bcolors.ENDC)

headers = {
    "User-Agent": 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

print("Looking for: " + itemToFind + "\n--------------------------------- Server response "
                                     "------------------------")

page = requests.get(URL, headers=headers)

if page.status_code == 200:
    print("status code: ", bcolors.OKBLUE + str(page.status_code) + bcolors.ENDC)
else:
    print("status code: ", bcolors.FAIL + str(page.status_code) + bcolors.ENDC)

soup = BeautifulSoup(page.text, 'lxml')

foundItem = 0

print("Item to find: ", itemToFind)

div = soup.find('div', class_='s-main-slot s-result-list s-search-results sg-row')
divChildren = div.findChildren('div', recursive=False)

itemCounter = 0

itemToFind = re.sub('[^A-Za-z0-9]+', ' ', itemToFind)

for child in divChildren:
    foundItemThis = 0
    for img in child.find_all('img',
                            alt=True):
        itemName = img['alt']
        itemName = re.sub('[^A-Za-z0-9.,]+', ' ', itemName)
        print(itemName)
        if re.search(r'.*' + itemToFind + '.*', itemName, re.IGNORECASE):
            print(bcolors.OKBLUE + "--------------------------------- FOUND! ---------------------------------" + bcolors.ENDC)
            print(bcolors.OKGREEN + img['alt'] + bcolors.ENDC)
            foundItem = 1
            foundItemThis = 1
    if foundItemThis == 1:
        spanPrice = child.find('span', class_='a-price')
        if spanPrice:
            price = spanPrice.find('span', class_='a-offscreen')
            print(bcolors.BOLD + price.text + bcolors.ENDC)
        for span in child.find_all('span', class_='aok-inline-block s-image-logo-view'):
            print(bcolors.UNDERLINE + "Available with prime!" + bcolors.ENDC)

# for div in soup.find_all('div',
#                          class_='sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 '
#                                 'sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28'):
#     foundItemThis = 0
#     for img in div.find_all('img',
#                             alt=True):
#         if re.search(r'.*' + itemToFind + '.*', img['alt'], re.IGNORECASE):
#             print(bcolors.OKBLUE + "FOUND!" + bcolors.ENDC)
#             print(bcolors.OKGREEN + img['alt'] + bcolors.ENDC)
#             foundItem = 1
#             foundItemThis = 1
#     if foundItemThis == 1:
#         spanPrice = div.find('span', class_='a-price')
#         if spanPrice:
#             price = spanPrice.find('span', class_='a-offscreen')
#             print(bcolors.BOLD + price.text + bcolors.ENDC)
#         for span in div.find_all('span', class_='aok-inline-block s-image-logo-view'):
#             print(bcolors.UNDERLINE + "Available with prime!" + bcolors.ENDC)

if foundItem == 0:
    print(bcolors.WARNING + "No items found!" + bcolors.ENDC)

print(bcolors.BOLD + "finished..." + bcolors.ENDC)
input(bcolors.HEADER + "Press Enter to continue..." + bcolors.ENDC)
