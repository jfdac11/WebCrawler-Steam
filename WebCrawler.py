import scrapy
from bs4 import BeautifulSoup as soup
import requests
from urllib.request import urlopen as uReq
from time import sleep
import cx_Oracle as cx
import mysql.connector
from mysql.connector import errorcode

try:
    db_connection = mysql.connector.connect(
        host='localhost', user='root', password='123', database='steamdb', auth_plugin='mysql_native_password')
    print("Database connection made!")
except mysql.connector.Error as error:
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User name or password is wrong")
    else:
        print(error)

mycursor = db_connection.cursor()
'''
mycursor.execute(
    "CREATE TABLE Names (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
'''
page = requests.get('https://store.steampowered.com/?l=portuguese')
Soup = soup(page.text, 'html.parser')

# Remover links inferiores
last_links = Soup.find(class_='carousel_container paging_capsules')
last_links.decompose()
# Pegar todo o texto da div BodyText
game_name_list = Soup.find("div", {"id": "tab_newreleases_content"})

# Pegar o texto de todas as instâncias da tag <a> dentro da div BodyText
game_name_list_items = game_name_list.find_all('div', {"class":"tab_item_name"})
for game_name in game_name_list_items:
    names = game_name.contents[0]
    print(names)
    mycursor.execute(
        "INSERT INTO Names (name) values ('{}')".format(names))
'''
Referência:
https://www.digitalocean.com/community/tutorials/como-fazer-scraping-em-paginas-web-com-beautiful-soup-and-python-3-pt
'''