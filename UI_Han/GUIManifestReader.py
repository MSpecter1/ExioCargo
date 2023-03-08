import tkinter as tk
# root = tk.Tk()

class container:
    def __init__(self, name, x, y, weight):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight

        if(self.name == "UNUSED"): #0 means "UNUSED"
                self.button = tk.Button(text=name, height=5, width=10, bg='white',activebackground='lightgrey')

        elif(self.name == "NAN"):
                self.button = tk.Button(text="NAN", height=5, width=10, bg='black',activebackground='black')

        else:
                self.button = tk.Button(text=name, height=5, width=10, bg='blue',activebackground='lightgrey')

    def display_info(self):
        print("Position: [",self.x,",", self.y,"], Weight:", self.weight ,"kg, Name:",self.name)

    def getName(self):
        return self.name



def read_manifest(file):
        containers = []
        with open(file) as f:
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
                # create container
                containers.append(container(n,x,y,w))
        print(len(containers))
        # for i in range(len(containers)):
        #     print(containers[i].name, containers[i].weight)

        return containers
                
def main():
    # gridSetup()
    file = "ShipCase2.txt"
    read_manifest(file)


if __name__ == '__main__':
    main()