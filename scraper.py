from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import from webdriver_manager (using underscore)
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3

# Store data in db
def store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link):
    conn = sqlite3.connect('amazon_search.db')
    curr = conn.cursor()

    # create table
    curr.execute(
        '''CREATE TABLE IF NOT EXISTS search_result (ASIN text, name text, price real, ratings integer, ratings_num text, details_link text)''')
    # insert data into a table
    curr.executemany(
        "INSERT INTO search_result (ASIN, name, price, ratings, ratings_num, details_link) VALUES (?,?,?,?,?,?)",
        list(zip(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)))

    conn.commit()
    conn.close()


# Get data fxn
def scrape_page(driver):
    product_name = []
    # ASIN number is used to unqiuely identify Amazon product
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

    for item in items:
        # get product name
        name = item.find_element_by_xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]')
        product_name.append(name.text)
        # get product asin (unique identifier)
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        # find prices
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
        # some products don't have a price so error handle
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

        # find a ratings box
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        if ratings_box:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings, ratings_num = 0, 0
        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))

        # find link
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_link.append(link)

    # following print statement is for checking that we correctly scrape data we want
    # print(product_name)
    # print(product_asin)
    # print(product_price)
    # print(product_ratings)
    # print(product_ratings_num)
    # print(product_link)

    # store data from lists to database
    store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)
    global next_page
    next_page = driver.find_element(By.XPATH, './/a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').get_attribute("href")
    # print('Next page is = ')
    # print(next_page)
    # / html / body / div[1] / div[2] / div[1] / div[1] / div / span[1] / div[1] / div[65] / div / div / span / a[1]
    # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[65]/div/div/span/a[1] s-pagination-item


def scrape_amazon(keyword, max_pages):
    page_number = 1

    # create a driver object using driver_path as a parameter
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # assign your website to scrape
    web = 'https://www.amazon.com'
    driver.get(web)

    # create WebElement for a search box
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    # type the keyword in search box
    search_box.send_keys(keyword)
    # create WebElement for a search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    # click search_button
    search_button.click()
    # wait for the page to download
    driver.implicitly_wait(5)

    while page_number <= max_pages:
        scrape_page(driver)
        page_number += 1
        driver.get(next_page)
        driver.implicitly_wait(5)
    # keep this line of code at the bottom
    driver.quit()


if __name__ == '__main__':
    # assign any keyword for searching and max number of pages
    scrape_amazon('espresso machine', 3)
