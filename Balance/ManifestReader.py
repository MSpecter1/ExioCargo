class container:
    container = False
    nan = False

    def __init__(self, name, x, y, weight, container, nan):
    # def __init__(self, name, x, y, weight):
        self.name = name
        self.x = x-1
        self.y = y-1
        self.weight = weight
        self.container = container
        self.nan = nan

    def display_info(self):
        print("Position: [",self.x,",", self.y,"], Weight:", self.weight ,"kg, Name:",self.name)

    def getName(self):
        return self.name
    
    def __eq__(self, other):
        # return (self.name==other.name and self.weight == other.weight and self.x == other.x and self.y == other.y)
        return (self.name==other.name and self.weight == other.weight)   
    def __lt__(self, other):
        return self.weight < other.weight

    def getRow(self):
        return self.x
    
    def getCol(self):
        return self.y

    def getWeight(self):
        return self.weight

class manifest_reader:
    manifest = None
    
    def set_manifest(self, manifest_link):
        self.manifest = manifest_link

    def read_manifest(self):
        containers = []
        with open(self.manifest) as f:
            # Per line
            while True:
                line = f.readline()
                if not line:
                    break
                line=line.strip()
                # X
                x=int(line[1:3]) 
                # Y
                y=int(line[4:6])
                # Weight - kilograms
                w=int(line[10:15])
                # Name
                n=(line[18:])

                c=False
                nan = False
                if w != 0:
                    c = True
                if n == 'NAN' and w==0:
                    nan = True

                containers.append(container(n,x,y,w,c,nan))

                # create container
                # containers.append(container(n,x,y,w))
        return containers
