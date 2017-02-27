from collections import defaultdict
import time

class FamousJapaneseDeathsDetector:

    def __init__(self, tweet_stream, tweet_classifier, japanese_name_extractor, threshold, period):
        self.tweet_stream = tweet_stream
        self.tweet_classifier = tweet_classifier
        self.japanese_name_extractor = japanese_name_extractor
        self.passed_list = []
        self.name_count = defaultdict(int)
        self.threshold = threshold
        self.period = period
        self.__calculate_reset_time()

    def famous_deaths(self):

        for text in self.tweet_stream.tweets():

            if time.time() >= self.reset_time:
                self.__calculate_reset_time()
                self.name_count = defaultdict(int)

            if self.tweet_classifier.is_death_related(text):
                name_list = self.japanese_name_extractor.get_japanese_names(text)
                if name_list:
                    for name in name_list:
                        if name not in self.passed_list:
                            self.name_count[name] += 1
                            if self.name_count[name] >= self.threshold:
                                self.passed_list.append(name)
                                yield name

    def __calculate_reset_time(self):
        self.reset_time = time.time() + self.period
