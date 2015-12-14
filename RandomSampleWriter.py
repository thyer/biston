import random

__author__ = 'Trent'


class RandomSampleWriter:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.MAX_REVIEWS = 5000
        with open(filename) as file:
            for line in file:
                if random.randint(1,1000) < 50:
                    self.data.append(line)
                if len(self.data) > self.MAX_REVIEWS:
                    break
        f = open("random" + str(self.MAX_REVIEWS) + ".json", "w+")
        for line in self.data:
            f.write(str(line))


def main():
    dp = RandomSampleWriter("data/yelp_academic_dataset_review.json")
    print("done")

if __name__ == '__main__':
    main()