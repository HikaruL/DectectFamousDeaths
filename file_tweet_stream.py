import re


class FileTweetStream:

    def __init__(self, filename):
        self.filename = filename

    def tweets(self):
        with open(self.filename) as f:
            for line in f.readlines():
                line = re.sub(r'\n', '', line)
                line = re.sub(r'RT @.+: ', '', line)
                yield line
