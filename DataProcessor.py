from JSONLoader import JSONLoader

__author__ = 'Trent'


class DataProcessor:
    def __init__(self, json_loader=None):
        if json_loader is None:
            json_loader = JSONLoader("bad_testing.json")
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
        item.obfuscation = self.calc_obfuscation(item.text)
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
        return len(text)

    def calc_obfuscation(self, text):
        # not sure what we want here
        return len(text)

    def calc_numerals(self, text):
        # lots of possibilities here
        return len(text)

    def calc_superlatives(self, text):
        # perhaps draw from a list, need to make sure -er isn't the only requisite
        return len(text)

    def calc_func_word_rate(self, text):
        # function words come from a list? Or parse through them?
        return len(text)

    def calc_deixis(self, text):
        # list? or parsed out?
        return len(text)

    def calc_word_count(self, text):
        # should be easy enough, just count the whitespace delimited character strings
        return len(text)

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
