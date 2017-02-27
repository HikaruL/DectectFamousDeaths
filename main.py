from file_tweet_stream import FileTweetStream
from tweet_stream import TweetStream
from famous_japanese_death_detector import FamousJapaneseDeathsDetector
from maxent_classify import MaxEntTweetClassifier
from extract_name import RomanizedJapaneseNamesExtractor
from twitter import Api

ACCESS_TOKEN = '93130558-dO7HqvIOEr3K3m5fJV087VZ73RN0gaEaYkUWgWe4Y'
ACCESS_SECRET = 'Ro0zxJPCOJExF6Vyy80NypFhanpA9twEvhUIzkS6OwmsU'
CONSUMER_KEY = 'N3XWvJDOcOt7eUqteJpLySANQ'
CONSUMER_SECRET = 'Jpi0Q2fIqA06CKzz0BFwRd77QOSE6u8WHjOrR03coZvwO3RVEj'
api = Api(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_SECRET)

# choose from twitter stream or file stream
twitter_stream = TweetStream(api, ['Japanese'], ['en'])
file_stream = FileTweetStream('maxEnt_model/training_tweets.txt')
tweet_classifier = MaxEntTweetClassifier('maxEnt_model/maxEnt_classifier.txt')
japanese_name_extractor = RomanizedJapaneseNamesExtractor()
# threshold: the minimum number of death tweets to reach within period to be considered as 'famous'
threshold = 10
# period: with which threshold must be reached, after period reached, count is reset to zero. unit: second
period = 60 * 60 * 24

# main function
# replace the file_stream with twitter_stream to get data from twitter api.
famous_japanese_deaths_detector = FamousJapaneseDeathsDetector(
    file_stream, tweet_classifier, japanese_name_extractor, threshold, period)

# output the names
f_out = open("passed_list.txt", 'a')
for name in famous_japanese_deaths_detector.famous_deaths():
    print(name + ' has passed away :(')
    f_out.write(name + ' has passed away :(\n')
