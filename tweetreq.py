from time import sleep
import random
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from datetime import timedelta as td
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse_tweet(card):

    try:
        postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime')
    except:
        postdate = None

    try:
        promoted = card.find_element(By.XPATH, './/div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = None
    
    try:
        element = card.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        tweet_url = None

    tweet = (postdate, tweet_url, promoted)
    
    return tweet


def get_driver():
    
    options = Options()    
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--profile-directory=Default')

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(100)
    return driver


def open_page(driver, since, hashtag):

    general_url = 'https://twitter.com/search?q='
    
    end_date = dt.strftime(since + td(days=2), 'until%%3A%Y-%m-%d')
    start_date = dt.strftime(since - td(days=2), 'since%%3A%Y-%m-%d%%20')

    hash_tags = "(%23" + hashtag + ")%20"
    path = general_url + hash_tags + start_date + end_date + '&src=typed_query&f=live'

    driver.get(path)


def scroll(driver):

    scroll_attempt = 0

    while True:
        sleep(random.uniform(0.5, 1.5))
        last_position = driver.execute_script("return window.pageYOffset;")
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            if scroll_attempt >= 60:
                print('FAIL')
                return False
            else:
                sleep(random.uniform(0.5, 1.5))  # attempt another scroll
        else:
            return True

def count_tweets(tweets):

    data = dict()

    for tweet in tweets:
        tweet_date = dt.strptime(tweet[0], '%Y-%m-%dT%H:%M:%S.000Z')
        rounded_time = tweet_date - td(seconds=tweet_date.second)
        if rounded_time not in data:
            data[rounded_time] = 1
        else:
            data[rounded_time] += 1

    return data

def get_tweets(driver):

    tweets = set()

    while True:
        sleep(random.uniform(0.5, 1.5))
        page_cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')  # changed div by article
        for card in page_cards:
            tweet = parse_tweet(card)
            if tweet and tweet not in tweets:
                tweets.add(tweet)
                print(tweet[0], tweet[1])
        
        if not scroll(driver):
            return count_tweets(tweets)            


def scrape(since, hashtag):
    
    driver = get_driver()
    
    open_page(driver=driver, since=since, hashtag=hashtag)
    print(get_tweets(driver))
    
    driver.close()

if __name__ == '__main__':
    scrape(since=dt(year=2022, month=1, day=27), hashtag='bitcoin')