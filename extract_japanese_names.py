import subprocess

# extract Japanese names from Japanese text
class JapaneseNamesExtractor:

    def __init__(self, classpath):
        self.classpath = classpath

    def get_japanese_names(self, sentence):
        stdoutdata = subprocess.getoutput(
            "java -classpath " + self.classpath + ":" + self.classpath +
            "/kuromoji-0.7.7.jar myextractor.JapaneseNamesExtractor " + sentence)
        return stdoutdata.split(",")

sentence = '私の名前は長島みか'
print(JapaneseNamesExtractor('.').get_japanese_names(sentence))