from nltk.tokenize import word_tokenize
import re

# the script is used to convert the training tweets into feature form

f_out = open("test.txt", 'w')
with open('test_tweets') as f_train:
    train_lines = f_train.readlines()
label = 'related '
for line in train_lines:
    line = line.strip()
    if line.startswith("CLASSLABEL = 2"):
        label = 'not.related '
        continue
    line = re.sub(r'RT @.+: ', '', line)
    word_list = word_tokenize(line)
    word_dict = {}
    instance_vector = []
    for word in word_list:
        matchObj = re.match(r'[\'\.\-\w]+', word)
        if matchObj:
            word_dict[word] = '1'
    for w, c in word_dict.items():
        instance_vector.append(w + ':' + c)
    instance = label + ' '.join(instance_vector) + '\n'
    f_out.write(instance)
