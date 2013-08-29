import shlex
import ConfigParser


## Custom Components Fields must start from 4
class EESchemaField(object):
    def __init__(self, number, text,  name="", orientation="H", posx="0", posy="0", size="50", flags="0000",hjustify="L", vjustify_italic_bold="CNN"):
        self.number= number
        self.text = text
        self.name = name
        self.orientation=orientation
        self.posx = posx
        self.posy = posy
        self.size=size
        self.flags=flags
        self.hjustify=hjustify
        self.vjustify_italic_bold = vjustify_italic_bold

    def __str__(self):
        n = ''
        if self.name != "":
            n = '"' + self.name + '"'
        return 'F {0} "{1}" {2} {3} {4} {5} {6} {7} {8} {9}'.format(
            self.number, self.text, self.orientation, self.posx, self.posy,
            self.size, self.flags, self.hjustify, self.vjustify_italic_bold,
            n)
    
class EESchemaComponent(object):
    def __init__(self, name, ref, N, mm="1", timestamp="0", position=(0,0), fields=[], aux=["",""]):
        self.name = name
        self.ref = ref
        self.fields = fields
        self.position=position
        self.N = N
        self.mm = mm
        self.timestamp = timestamp
        self.aux = aux # NEED TO PARSE THIS
        self.__format__ = """
$Comp
L {0} {1}
U {2} {3} {4}
P {5} {6}
{7}
{8}$EndComp""".format( self.name, self.ref, self.N, self.mm, self.timestamp,
                       self.position[0], self.position[1],
                       "\n".join([str(field) for field in fields]), "".join(aux))

#        print self.__format__,
        
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
        pos = [0,0]
        N = ""
        mm = ""
        timestamp = ""
        aux = []
        for i in self.f.readlines():

            if "$Comp" in i:
                in_comp = 1
                ref = 0
                name = ""
                fields = []
                ref = 0
                name = ""
                fields = []
                pos = [0,0]
                N = ""
                mm = ""
                timestamp = ""
                aux = []
            elif "$EndComp" in i:
#                if ref[0] != "#":
                self.components.append( EESchemaComponent( name, ref, N ,mm,timestamp,pos, fields, aux) )
                in_comp = 0
            elif in_comp:
                if i[0] == "L":
                    name = i.split()[1]
                    ref = i.split()[2]
                elif i[0] == "U":
                    N = i.split()[1]
                    mm = i.split()[2]
                    timestamp = i.split()[3]
                elif i[0] == "P":
                    pos[0] = int(i.split()[1])
                    pos[1] = int(i.split()[2])
                elif i[0] == "F":
                    field_arr = shlex.split(i)

                    if (len(field_arr) == 11):
                        n = field_arr[10]
                    else:
                        n = ""
                    fields.append(EESchemaField(
                        number=field_arr[1],
                        text=field_arr[2],
                        name=n,
                        orientation=field_arr[3],
                        posx=int(field_arr[4]),
                        posy=int(field_arr[5]),
                        size=int(field_arr[6]),
                        flags='0000'))
                else:
                    aux.append(i)
        
    def __str__(self):
        return "".join(["{0}\n".format(str(c)) for c in self.components])
    
if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.readfp(open("default.cfg"))

    print config.get('Octopart', 'api_key')
    a = EESchemaSCHFile("artemis-synth.sch")
    a.open()
    a.parseComponents()
    a.close()

#    print a

