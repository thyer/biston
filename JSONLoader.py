import json
import sys

__author__ = 'Trent'


class JSONLoader:
    def __init__(self, filename):
        self.data = []
        self.currentReview = 0
        with open(filename) as file:
            ticker = 0
            self.reviews = []
            for line in file:
                self.reviews.append(json.loads(line))
                ticker += 1
                if ticker % 10000 == 0: # helps break up large files to keep memory requirements down
                    print(str(ticker) + " lines processed")
                    self.process()
                    self.reviews = []
        self.process()
        self.reviews = []

    def process(self):
        print("Processing")
        error = ""
        for review in self.reviews:
            if 'review_id' not in review:
                error += " review_id, "
            if 'text' not in review:
                error += "text, "
            if 'stars' not in review:
                error += "stars, "
            if 'votes' not in review or 'useful' not in review['votes']:
                error += "votes/useful "
            if error is not "":
                error = "The fields " + error + " etc. were missing from the review: "
                error += "\n" + str(review)
                sys.exit(error)

            id = review['review_id']
            text = review['text']
            stars = review['stars']
            useful = review['votes']['useful']
            # need to decide what other information is interesting to us

            self.data.append([id, text, stars, useful])

    def get_next_review(self):
        if self.currentReview >= len(self.data):
            return None
        out = self.data[self.currentReview]
        self.currentReview += 1
        return out

    def get_all_reviews(self):
        return self.data


def main():
    js = JSONLoader("testing.json")
    print("done")

if __name__ == '__main__':
    main()
