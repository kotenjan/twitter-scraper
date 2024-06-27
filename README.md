# Twitter Hashtag Scraper

This script scrapes tweets containing a specific hashtag from Twitter within a given date range. It extracts tweet information such as the post date, tweet URL, and promotion status, and counts the number of tweets per minute.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver

## Setup

1. Install the required Python packages:
    ```sh
    pip install selenium
    ```

2. Download Chrome WebDriver and ensure it is in your system PATH or specify its location in the script.

## Usage

### Function Definitions

- **`parse_tweet(card)`**: Extracts the post date, tweet URL, and promotion status from a tweet card element.
- **`get_driver()`**: Configures and returns a headless Chrome WebDriver instance.
- **`open_page(driver, since, hashtag)`**: Constructs the search URL based on the hashtag and date range, and opens the page using the WebDriver.
- **`scroll(driver)`**: Scrolls the Twitter page to load more tweets.
- **`count_tweets(tweets)`**: Counts the number of tweets per rounded minute from the set of tweets.
- **`get_tweets(driver)`**: Collects tweets from the page and calls `parse_tweet` to extract tweet information.
- **`scrape(since, hashtag)`**: Main function to initialize the driver, open the page, get tweets, and close the driver.

### Running the Script

To run the script, execute the following command in your terminal:
```sh
python script.py
```

Replace `script.py` with the actual name of your script file.

### Example Usage

```python
if __name__ == '__main__':
    scrape(since=dt(year=2022, month=1, day=27), hashtag='bitcoin')
```

This example will scrape tweets containing the hashtag `#bitcoin` from around January 27, 2022.

## Notes

- Ensure that the WebDriver is compatible with your version of Chrome.
- The script uses a headless browser for scraping, which means it runs without a graphical user interface.
- The `scroll` function attempts to load more tweets by scrolling the page up to 60 times if necessary.

## License

This project is licensed under the MIT License.
