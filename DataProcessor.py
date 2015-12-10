from JSONLoader import JSONLoader

__author__ = 'Trent'


import re

class DataProcessor:
    def __init__(self, json_loader=None):
        if json_loader is None:
            json_loader = JSONLoader("testing.json")
        self.json_loader = json_loader
        self.data = []

        next_review = self.json_loader.get_next_review()
        while next_review is not None:
            self.process(next_review)
            next_review = self.json_loader.get_next_review()

        print("Done processing, total reviews: " + str(len(self.data)))

    def process(self, review):
        item = ReviewItem(review[0])
        item.text = review[1]
        item.stars = review[2]
        item.usefulness = review[3]
        # TODO: implement all of these methods
        item.alpha_ratio = self.calc_alpha_ratio(item.text)
        item.punctuation_frequency = self.calc_punct_frequency(item.text)
        # item.obfuscation = self.calc_obfuscation(item.text)
        item.numerals = self.calc_numerals(item.text)
        item.superlative_comparative = self.calc_superlatives(item.text)
        item.function_word_rate = self.calc_func_word_rate(item.text)
        item.deixis = self.calc_deixis(item.text)
        item.char_count = len(item.text)
        item.word_count = self.calc_word_count(item.text)
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
            
        avgWordLength = ((wordLengthSum * 1.0) / len(textWords))
            
        
        
        # Split the text at the .'s in order to separate into sentences
        sentenceSplitText = text.split(".")
        sentenceSplitText = sentenceSplitText.split(";")
        sentenceSplitText = sentenceSplitText.split(", and ")
        sententeSplitText = sentenceSplitText.split(", but ")
        sentenceCount = 1
        
        # If sentences exist (i.e. text is NOT empty), then proceed with processing
        if len(sentenceSplitText) > 0:
            
            sentenceLengthSum = 0
            
            for sentence in sentenceSplitText:
                sentenceLengthSum += len(sentence)
                
                sentenceCount += 1
                
            avgSentenceLength = ((sentenceLengthSum * 1.0) / sentenceCount)
            
            
        return len(text)

    
    def calc_numerals(self, text):
        # lots of possibilities here
        numerals = 0
        for word in text:
            if re.search(".*\d+.*", word):
                numerals += 1
        return len(text)

    
    def calc_superlatives(self, text):
        # perhaps draw from a list, need to make sure -er isn't the only requisite
        #without tagging for POS or pronunciation it will be difficult to get this just right - I'm going to use a regex looking for everything ending in a Cest or Ciest
        #I tried looking for C's that we could maybe exclude, but there weren't really any
        #this will cause problems for some words that end in these, but I don't think there will be too many that will be very common

        textLower = text.lower()
        for word in textLower:
            #superlatives
            if re.search("(.*[b||c||d||f||g||h||j||k||l||m||n||p||q||r||s||t||v||w||x||z]+(est|iest)|(most)|(least)|(worst))", word):
                superlative_comparative += 1
            #comparatives
            elif re.search("(.*[b||c||d||f||g||h||j||k||l||m||n||p||q||r||s||t||v||w||x||z]+(er|ier)|(more)|(less[er]*)|(worse))", word):
                superlative_comparative += 1

        return len(text)

    
    def calc_func_word_rate(self, text):
        # function words come from a list? Or parse through them?
        # Fucntion words come from a text file, which is read in as a string, and forced to lower case,
        # then each word in text (forced to lower case) is checked for whether it is in the "function word string"
        exclusionWords = open ("exclusionWords.txt", "r")
        exclusionString = exclusionWords.read().lower()
        
        functionWordCount = 0
        nonFunctionWordCount = 0
        
        textLower = text.lower()
        
        for word in textLower:
        
            if word in exclusionString:
                functionWordCount += 1
                
            else:
                nonFunctionWordCount += 1
            
        
        return len(text)

    def calc_deixis(self, text):
        # list? or parsed out?
        deicticWords = open ("deixix.txt", "r")
        deicticString = deicticWords.read().lower()

        deixis = 0

        textLower = text.lower()

        for word in textLower:
            if word in deicticString:
                deixis += 1

        #do we want to account for phrases as well??? i.e. next year, last week etc...
        return len(text)

    def calc_word_count(self, text):
        # should be easy enough, just count the whitespace delimited character strings
        
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
