import re


class TweetStream:

    def __init__(self, api, track, languages):
        self.api = api
        self.track = track
        self.languages = languages

    def tweets(self):
        for tweet in self.api.GetStreamFilter(track=self.track, languages=self.languages):
            if 'text' in tweet:
                text = tweet['text']
                text = re.sub(r'\n', '', text)
                text = re.sub(r'RT @.+: ', '', text)
                yield text
