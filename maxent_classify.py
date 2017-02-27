import math
import re
from nltk.tokenize import word_tokenize


# a maxEnt classifier to check if a tweet is death related or not.
class MaxEntTweetClassifier:

    def __init__(self, model_file):
        self.model = self.__initialize_model(model_file)

    # initialize the maxEnt model for later use
    def __initialize_model(self, model_file):
        with open(model_file, encoding="ISO-8859-1") as f_model:
            model_lines = f_model.readlines()
        label_hash = {}
        feature_hash = {}
        model_dict = {}
        label_index = -1
        feature_index = 0
        for line in model_lines:
            if not line:
                continue
            line = line.strip()
            if line.startswith("FEATURES FOR CLASS"):
                label_index += 1
                line = line.strip("FEATURES FOR CLASS")
                new_label = line.strip()
                label_hash[new_label] = label_index
            elif line.startswith("<default>"):
                default_value = float(line.split(' ')[1])
                if 'default' not in model_dict:
                    model_dict['default'] = {}
                model_dict['default'][label_index] = default_value
            else:
                pair = line.split(' ')
                feature = pair[0]
                feature_value = float(pair[1])
                if feature not in feature_hash:
                    feature_hash[feature] = feature_index
                    feature_index += 1
                featurei = feature_hash[feature]
                if featurei not in model_dict:
                    model_dict[featurei] = {}
                model_dict[featurei][label_index] = feature_value
        label_hash_reverse = {}
        for label, index in label_hash.items():
            label_hash_reverse[index] = label
        return label_hash, feature_hash, model_dict, label_hash_reverse

    # calculate the prob for related or not related and choose the higher one.
    # return true if it is related, the test data is a feature vector.
    def __maxent_decoding(self, test_data):
        label_hash, feature_hash, model_dict, label_hash_reverse = self.model
        line = test_data.strip()
        result_hash = {}
        for k, v in label_hash.items():
            result_hash[v] = model_dict['default'][v]
        line_list = re.split(" +", line)
        for i in range(0, len(line_list)):
            pair = line_list[i]
            pair_list = pair.split(':')
            feature = pair_list[0]
            if feature in feature_hash:
                for k, v in result_hash.items():
                    result_hash[k] += model_dict[feature_hash[feature]][k]
        for k, v in result_hash.items():
            result_hash[k] = math.exp(result_hash[k])
        result_hash = sorted(result_hash.items(), key=lambda x:x[1], reverse=True )
        predict_label = result_hash[0][0]
        z = 0
        for kv_tuple in result_hash:
            z += kv_tuple[1]
        if label_hash_reverse[predict_label] == 'related':
            return True
        else:
            return False

    # get the feature vector for a given tweet text
    def __get_feature_vector(self, text):
        word_list = word_tokenize(text)
        word_dict = {}
        instance_vector = []
        for word in word_list:
            matchObj = re.match(r'[\'\.\-\w]+', word)
            if matchObj:
                word_dict[word] = '1'
        for w, c in word_dict.items():
            instance_vector.append(w + ':' + c)
        feature_vector = ' '.join(instance_vector)
        return feature_vector

    # check if a tweet is death related using maxEnt model
    def is_death_related(self, tweet_text):
        # tweet_text = 'Rest:1 in:1 peace:1 ...:1 We:1 will:1 never:1 forget:1 you:1 .:1 https:1'
        feature_vector = self.__get_feature_vector(tweet_text)
        return self.__maxent_decoding(feature_vector)
