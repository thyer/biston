from JSONLoader import JSONLoader
from UsefulnessArffLoader import UsefulnessArffLoader
import re

__author__ = 'Trent'


class DataProcessor:
    def __init__(self, json_loader=None):
        self.pivot = 5
        self.proportional = True
        self.nominalize_usefulness = True
        if json_loader is None:
            json_loader = JSONLoader("random20000.json", self.proportional, self.pivot)
        self.json_loader = json_loader
        self.data = []
        self.ticker = 0

        next_review = self.json_loader.get_next_review()
        while next_review is not None:
            self.process(next_review)
            next_review = self.json_loader.get_next_review()

        string_file = "yelp_"
        if self.proportional:
            string_file += "prop_pivot" + str(self.pivot) + "_"
        if self.nominalize_usefulness:
            string_file += "nom_"
        else:
            string_file += "cont_"
        string_file += str(len(self.data)) + "reviews"
        arff_loader = UsefulnessArffLoader(string_file)
        schema = 'id', 'text', 'stars', 'alpha_ratio', 'punctuation_frequency', \
                                'obfuscation', 'numerals', 'function_word_rate', 'deixis',\
                                'word_count', 'usefulness'
        arff_loader.load_schema(schema)
        for item in self.data:
            arff_loader.load_line(item)
        arff_loader.write_to_file()

        print("Done processing, total reviews: " + str(len(self.data)))

    def process(self, review):
        self.ticker += 1
        if self.ticker % 1000 == 0:
            print(str(self.ticker) + " reviews processed in DataProcessor")
        item = ReviewItem(review[0])
        item.text = review[1]
        item.stars = review[2]
        # TODO: implement all of these methods
        item.alpha_ratio = self.calc_alpha_ratio(item.text)
        item.punctuation_frequency = self.calc_punct_frequency(item.text)
        item.obfuscation = self.calc_obfuscation(item.text)
        item.numerals = self.calc_numerals(item.text)
        item.function_word_rate = self.calc_func_word_rate(item.text)
        item.deixis = self.calc_deixis(item.text)
        item.word_count = self.calc_word_count(item.text)
        usefulness = review[3]
        if self.nominalize_usefulness:
            if usefulness >= self.pivot:
                item.usefulness = 1
            else:
                item.usefulness = 0
        else:
            item.usefulness = usefulness
        self.data.append(item)

    def calc_alpha_ratio(self, text):
        alpha = 0
        chars = 0
        for char in text:
            if char.isalpha():
                alpha += 1
            chars += 1
        return alpha/chars

    def calc_punct_frequency(self, text):
        # try looking at string.punctuation here
        
        punctuation_count = 0
        char_count = 0
        
        for char in text:
            char_count += 1
            if char in "(),.!?--;{}[]<>:\'\"":
                punctuation_count += 1
        
        return punctuation_count/char_count

    def calc_obfuscation(self, text):
        # not sure what we want here
        # I think here we need to define some boundaries of "easy difficulty", "moderate difficulty", "high difficulty" in terms of readability
        # My guess is this will take into account things like sentence length, word length, punctuation, multiple negatives.
        multiNegCount = 0
        avgSentenceLength = 0
        avgWordLength = 0
        
        # Check for multiple negatives in the text, and simultaneously compute average word length
        index = 0
        wordLengthSum = 0
        
        textWords = re.sub ("\.|\;|\,|\--|\:|\?|\!|\(|\)|\{|\}|\[|\]", "", text)
        textWords = textWords.split()
        
        
        while index < len(textWords) - 1:
            wordLengthSum += len(textWords[index])
            
            if ("n't" in textWords[index] and textWords[index + 1].lower() == "not") or ("not" == textWords[index].lower() and "n't" in textWords[index+1]):
                multiNegCount += 1
                    
            index += 1
        if len(textWords) == 0:
            avgWordLength = 0
        else:
            avgWordLength = ((wordLengthSum * 1.0) / len(textWords))
            
        
        
        # Separate the text into sentences
        sentenceSplitText = re.split("\.|!|\?|\n|;|, and|, but", text)

        # If sentences exist (i.e. text is NOT empty), then proceed with processing
        if len(sentenceSplitText) > 0:
            
            sentenceLengthSum = 0
            sentenceCount = 1
            
            for sentence in sentenceSplitText:
                if len(sentence)> 0:
                    sentenceLengthSum += len(sentence)
                    sentenceCount += 1
                
            avgSentenceLength = ((sentenceLengthSum * 1.0) / sentenceCount)
            
        #Return the summation value discussed in email and class on 12/7/2015

        totalObfuscationSum = multiNegCount + avgWordLength + avgSentenceLength

        # Total Obfuscation Value is the numerical value that represents the category of the above sum (x)
        # For the above sum (X):
        # If X <= 11, then obfuscation = 1 = easy to read,
        # If 11 < X <= 17, then obfuscation = 2 = moderate to read
        # If 17 < X, then obfuscation = 3 = difficult to read

        discrete_obfuscation_value = 0

        if totalObfuscationSum <= 11:
            discrete_obfuscation_value = 1

        elif (11 < totalObfuscationSum) and (totalObfuscationSum <= 17):
            discrete_obfuscation_value = 2

        else:
            discrete_obfuscation_value = 3

        return totalObfuscationSum

    def calc_numerals(self, text):
        numerals = 0
        total = 0
        for word in text:
            total += 1
            if re.search(".*\d+.*", word):
                numerals += 1
        return numerals/total

    def calc_func_word_rate(self, text):
        # Function words come from a text file, which is read in as a string, and forced to lower case,
        # then each word in text (forced to lower case) is checked for whether it is in the "function word string"
        exclusionWords = open("exclusionWords.txt", "r")
        exclusionString = exclusionWords.read().lower()
        
        functionWordCount = 0

        textLower = text.lower()
        textLower = re.split("\.|!|\?|\n|;|,| ", textLower)
        words = 0
        
        for word in textLower:
            words += 1
            if word in exclusionString:
                functionWordCount += 1
        
        return functionWordCount / words

    def calc_deixis(self, text):
        deicticWords = open ("deixis.txt", "r+")
        deicticString = deicticWords.read().lower()
        deixis = 0
        words = 0
        textLower = text.lower()

        for word in textLower:
            words+=1
            if word in deicticString:
                deixis += 1

        #do we want to account for phrases as well??? i.e. next year, last week etc...
        return deixis/words

    def calc_word_count(self, text):
        splitText = text.split()
        return len(splitText)

    def reload_json(self, json_loader):
        self.json_loader = json_loader


class ReviewItem:
    def __init__(self, id):
        self.id = id


def main():
    dp = DataProcessor()
    print("done")

if __name__ == '__main__':
    main()
