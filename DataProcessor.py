from JSONLoader import JSONLoader

__author__ = 'Trent'


class DataProcessor:
    def __init__(self, json_loader=None):
        print("in constructor")
        if json_loader is None:
            json_loader = JSONLoader("yelp_academic_dataset_review.json")
        self.json_loader = json_loader
        self.data = []
        next_review = self.json_loader.get_next_review()
        while next_review is not None:
            self.process(next_review)

    def process(self, review):
        # here we'll want to actually do the processing and add features
        self.data.append(review)

    def reload_json(self, json_loader):
        self.json_loader = json_loader


def main():
    dp = DataProcessor()
    print("done")

if __name__ == '__main__':
    main()
