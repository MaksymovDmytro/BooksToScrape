import requests
from bs4 import BeautifulSoup as bs


def main() -> dict:
    data = {'scraped_books': []}
    url = f'http://books.toscrape.com/catalogue/'
    # Get page content in order to define number of total pages on website
    html_catalogue_page = requests.get(f'{url}page-1.html').content
    soup_catalogue_page = bs(html_catalogue_page, 'html.parser')
    total_pages = str(soup_catalogue_page.find('li', attrs={'class': 'current'})).split()[-2]
    # Iterating over pages
    for page_num in range(1, int(total_pages) + 1):
        page_link = f'page-{page_num}.html'
        # Get page content in order to get full item list
        html_catalogue_page = requests.get(f'{url}{page_link}').content
        soup_catalogue_page = bs(html_catalogue_page, 'html.parser')
        books_catalogue = soup_catalogue_page.find_all('article')

        for item in books_catalogue:
            # Composing full url an item and getting the content of the item page
            book_link = item.find('a')['href']
            html_book_page = requests.get(f'{url}{book_link}').content
            soup_book_page = bs(html_book_page, 'html.parser')
            # Finding proper html tag to get itme info
            book_info = soup_book_page.find('article')
            # Scraping info about an item
            title = book_info.find('h1').contents[0]
            rating = book_info.find('p', attrs={'class': 'star-rating'})['class'][1]
            price = book_info.find('p', attrs={'class': 'price_color'}).contents[0]
            # Description might be empty for some items so we need to assign empty value
            try:
                description = book_info.find('p', attrs={'class': ''}).contents[0]
            except AttributeError:
                description = 'Empty'

            category_breadcrumb = soup_book_page.find('ul', attrs={'class': 'breadcrumb'})
            category = category_breadcrumb.find_all('a')[2].contents[0]
            # Appending item info to a list of dicts
            data['scraped_books'].append({'title': title,
                                          'category': category,
                                          'rating': rating,
                                          'price': price,
                                          'description': description})
    return data


if __name__ == '__main__':
    print(main())
