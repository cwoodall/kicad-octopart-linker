import shlex

class EESchemaField(object):
    def __init__(self, number, text, name=""):
        self.number= number
        self.text = text
        self.name = name
        
class EESchemaComponent(object):
    def __init__(self, name, ref, fields=[]):
        self.name = name
        self.ref = ref
        self.fields = fields

    def __str__(self):
        a = ["\t{0}: {1}".format(f.name, f.text) for f in self.fields]
        
        return "{0} {1}\n{2}".format(self.ref, self.name, "\n".join(a))
        
class EESchemaSCHFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.f = None
        self.components = []
        
    def open(self):
        self.f = open(self.filename)

    def close(self):
        self.f.close()
        
    def parseComponents(self):
        in_comp = 0
        ref = 0
        name = ""
        fields = []
        for i in self.f.readlines():
            if in_comp:
                if i[0] == "L":
                    name = i.split()[1]
                    ref = i.split()[2]
                if i[0] == "F":
                    field_arr = shlex.split(i)

                    if (len(field_arr) == 11):
                        n = field_arr[10]
                    elif field_arr[1] == '0':
                        n = "Reference"
                    elif field_arr[1] == '1':
                        n = "Value"
                    else:
                        n = ""
                    fields.append(EESchemaField(field_arr[1], field_arr[2], n))
                       

            if "$Comp" in i:
                in_comp = 1
                ref = 0
                name = ""
                fields = []
            elif "$EndComp" in i:
                if ref[0] != "#":
                    self.components.append( EESchemaComponent( name, ref, fields ) )
                in_comp = 0
        
    def __str__(self):
        return "".join(["{0}\n".format(str(c)) for c in self.components])
    
if __name__ == "__main__":
    a = EESchemaSCHFile("artemis-synth.sch")
    a.open()
    a.parseComponents()
    a.close()

    print a

