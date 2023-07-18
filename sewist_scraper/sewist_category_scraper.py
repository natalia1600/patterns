import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.sewist.com/editor/mix/"
HTML_PARSER_INDEX = "html.parser"
SEWIST_CATEGORY_CLASS_IDENTIFIER = "select-snippet thumbnail"

def main():
    categories_dictionary = {}
    categories = get_categories_for_page()
    print(categories)


#  Given a URL from Sewist.com we map the categories to the ID
def get_categories_for_page(url=BASE_URL, categories_dictionary={}):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, HTML_PARSER_INDEX)
    f = open('sewist_category_ids.txt', 'a')

    categories_soup = soup.find_all("a", {"class" : SEWIST_CATEGORY_CLASS_IDENTIFIER})
    for category_soup in categories_soup:
        category_name = category_soup.select_one('div').text.strip()
        category_id = category_soup['href'].split('mix/')[-1]
        if category_name in categories_dictionary:
            # For now, do not do anything for duplicates
            # TODO: figure out Girl's sizing
            continue

        categories_dictionary[category_name] = category_id
        f.write(category_name + '; ' + category_id +'\n')

        if url == BASE_URL:
            url += category_id
        else:
            url += '-' + category_id
        print(url, categories_dictionary)
        categories_dictionary = get_categories_for_page(url, categories_dictionary)
    f.close()
    return categories_dictionary

main()
