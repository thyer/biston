import json

__author__ = 'Trent'


class JSONLoader:
    def __init__(self, filename):
        self.data = []
        self.currentReview = 0
        with open(filename) as file:
            ticker = 0
            self.reviews = []
            for line in file:
                if ticker % 100000 == 0:
                    print(line)
                self.reviews.append(json.loads(line))
                ticker += 1
                if ticker % 10000 == 0:
                    print(str(ticker) + " lines processed")
                    self.process()
                    self.reviews = []

    def process(self):
        for review in self.reviews:
            id = review['review_id']
            text = review['text']
            stars = review['stars']
            useful = review['votes']['useful']
            # need to decide what other information is interesting to us

            self.data.append([id, text, stars, useful])

    def get_next_review(self):
        out = self.data[self.currentReview]
        self.currentReview += 1
        if self.currentReview >= len(self.data):
            return None
        return out

    def get_all_reviews(self):
        return self.data


def main():
    js = JSONLoader("yelp_academic_dataset_review.json")
    print("done")

if __name__ == '__main__':
    main()
