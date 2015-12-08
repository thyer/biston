__author__ = 'Trent'

class ArffLoader:
    def __init__(self, filename=None):
        self.relation_name = filename.split(".")[0]
        self.schema = None
        self.data = None
        self.filename = filename
        if filename is None:
            self.filename = 'output.arff'
        print(filename + " instance created")

    def load_schema(self, schema):
        self.schema = schema

    def load_line(self, line):
        str_line = ""
        for field in self.schema:
            str_line += str(line.__dict__.get(field)) + ","

    def write_to_file(self):
        f = open(self.filename, 'w+')
        f.write("@relation " + self.relation_name)
        f.close()
