# Twitter Analyser

A simple web-app that depicts relevant Twitter data in the form of charts and graphs.

**Input** Hashtag related to a particular person or an event.
**Output** The following:
* Location of the the tweets.
* Popularity of the tweets in Delhi.
* Distribution of the original and retweeted tweets.
* Distribution of the favourite counts on the original and retweeted tweets.
* Distribution of the content in the tweets i.e. whether it is only text or text and image.
* Top 10 hashtags related to the tweet.

## Tools and Frameworks

|  |  |
| ------ | ------ |
| Django | Web app framework. |
| MongoDB | For the database. |
| Google Charts | For interactive graphs. |
| WordCloud | For generating word clouds. |
| NLTK | For sentiment analysis. |

* Django
* MongoDB
* Modules and Libraries
    - Google Charts *(for interactive graphs)*
    - Tweepy *(for extracting tweets)*
    - WordCloud *(for generating the word clouds)*
    - NLTK *(for sentiment analysis)*

## A walkthrough

1. **Location of the tweets:**
Extracted the location of the Twitter user (from where he or she has registered), since in most cases the geographical location i.e. the latitude and longitude had been disabled and the location of the Twitter user is not structured. The code can easily be updated to sustain and reflect structured location data.

2. **Popularity at a place:**
Currently, the input is New Delhi, but could be changed to any place. The popularity has been measured on the basis of the following factors:
    * Sentiment of the tweet
    * Retweet count
    * Favourite count
    * Popularity could be classified as either positive or negative. The gauge meter shows the particular number.
    *
3. **Top 10 Hashtags:**
Upon extraction of tweets with the required hashtags, we can scrap the other hashtags used in that particular tweet. However, we maintain a count of the hashtags in order to generate a word-cloud of most frequent hashtags.

4. **Distribution of Original Tweets vs Retweeted Tweets:**
After scraping the tweets, it is easy to categorise the retweeted tweets from the original tweets as the retweeted tweets have a property called `retweeted_status`. So, we can get the distribution of the original and retweeted tweets.

5. **Distribution of the Content in the tweets**
From the scraped tweets, we search for the `media` tag as it tells us if there were any media (image) attached to the tweet.

6. **Favourite Count on the Original Tweets**
From the scraped tweets, we can determine the Original and Retweeted Tweets (step 4). After that, we collect the `favourite_count` related to that particular tweet.

## Installation

* Clone the repository.
* Switch to the repository folder.
* Run the following command.

```sh
$ python manage.py runserver
```
