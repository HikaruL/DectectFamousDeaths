import nltk
from nameparser.parser import HumanName


# extract roman japanese names from English text
class RomanizedJapaneseNamesExtractor:

    def __get_human_names(self, text):
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        person_list = []
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
        return person_list

    # check if the name consists of Japanese syllables
    def __word_break(self, s, words):
        d = [False] * len(s)
        for i in range(len(s)):
            for w in words:
                if w == s[i-len(w)+1:i+1] and (d[i-len(w)] or i-len(w) == -1):
                    d[i] = True
        return d[-1]

    # check if the text contains names and return list of names
    def __check_if_japanese(self, text, syllables):
        name_list = []
        names = self.__get_human_names(text)
        for name in names:
            if self.__word_break(HumanName(name).last.lower(), syllables) and \
                    self.__word_break(HumanName(name).first.lower(), syllables):
                name_list.append(name)
        return name_list

    def get_japanese_names(self, text):
        # these are the syllables that can appear in Japanese names
        syllables = ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko', 'sa', 'shi', 'su', 'se', 'so',
                     'ta', 'chi', 'tsu', 'te', 'to', 'na', 'ni', 'nu', 'ne', 'no',
                     'ha', 'hi', 'fu', 'he', 'ho', 'ma', 'mi', 'mu', 'me', 'mo', 'ya', 'yu', 'yo',
                     'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'ga', 'gi', 'gu', 'ge', 'go',
                     'za', 'ji', 'zu', 'ze', 'zo', 'ba', 'bi', 'bu', 'be', 'bo',
                     'pa', 'pi', 'pu', 'pe', 'po', 'da', 'ji', 'du', 'de', 'do',
                     'kya', 'kyu', 'kyo', 'sha', 'shu', 'sho', 'cha', 'chu', 'cho', 'nya', 'nyu', 'nyo',
                     'hya', 'hyu', 'hyo', 'mya', 'myu', 'myo', 'rya', 'ryu', 'ryo', 'gya', 'gyu', 'gyo',
                     'ja', 'ju', 'jo', 'dya', 'dyu', 'dyo', 'bya', 'byu', 'byo', 'pya', 'pyu', 'pyo', 'n'
                     ]
        name_list = self.__check_if_japanese(text, syllables)
        return name_list
