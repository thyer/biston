__author__ = 'Trent'


class UsefulnessArffLoader:
    def __init__(self, filename=None):
        self.relation_name = filename.split(".")[0]
        self.schema = None
        self.data = []
        self.filename = filename
        if filename is None:
            self.filename = 'output.arff'
        print(filename + " instance created")

    def load_schema(self, schema):
        self.schema = schema

    def load_line(self, line):
        str_line = ""
        for field in self.schema:
            if 'text' in field or 'stars' in field or 'id' in field:
                continue
            str_line += str(line.__dict__.get(field)) + ","
        str_line = str_line[:-1] # strip off final comma
        self.data.append(str_line)

    def write_to_file(self):
        print("ArffLoader writing to disk")
        f = open(self.filename, 'w+')
        f.write("@relation " + self.relation_name + "\n")
        for field in self.schema:
            if 'text' in field or 'stars' in field or 'id' in field:
                continue
            f.write("@attribute " + field)
            if 'id' in field:
                f.write(" string\n")
            elif 'usefulness' in field:
                f.write(" {1, 0}\n")
            else:
                f.write(" numeric\n")
        f.write("@data\n")
        for line in self.data:
            f.write(line + "\n")
        f.close()
