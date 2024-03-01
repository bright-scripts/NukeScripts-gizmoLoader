#import nuke
import os

def main(): 

    dotNukePath = "C:/Users/Gigabyte/.nuke"
    path = dotNukePath+"/ToolSets/gizmoLoader"

    # Creating the gizmoLoader folder if it doesn't already exist
    if not os.path.isdir(path):
        os.makedirs(path)
        print("##############################\nNO FOLDER NAMED \"gizmoLoader\" HAS BEEN FOUND, creating it now.\n##############################")

    gizmos = discover(path)

    for x in gizmos:
        print(f"- {x}")

    org(path, gizmos)

    ### END OF main() ###

# Creating a class for organizing menus
class NukeMenu:
    def __init__(self, level, content):
        self.level = level
        self.content = content
    def __str__(self):
        return f"level: {self.level} | content: {self.content})"

# Function responsible for discovering gizmos
def discover(fromHere):
    # Discovering directories and files in `fromHere` folder
    discovery = os.walk(top=fromHere)

    # for x in discovery:
    #     print("[0] Dir path: " + x[0])
    #     print("[1] Dir names: ")
    #     for y in x[1]:
    #         print("- " + y)
    
    #     print("[2] File names: ")
    #     for y in x[2]:
    #         print("- " + y)
    #     print("-------------------")


    # Formatting discovery info into menus
    gizmos = []

    for x in discovery:
        # The line below replaces "/" found in windows' path format with "\", that python (and basically everything else?) uses.
        temp = x[0].replace("/", "\\").split("\\")
        temp = temp[temp.index("gizmoLoader")+1:] 

        for y in x[2]:
            temp.append(y)
            gizmos.append(temp)

    return gizmos
    ### END OF discover() ###

# Fonction responsible for organizing gizmos into menus
def org(path, gizmos):
    # Add PluginPaths to tools and icons
    nuke.pluginAddPath(f"'{path}'")

    # Create Gizmo Loader Menu
    toolbar = nuke.menu('Nodes')
    m = toolbar.addMenu('GizmoLoader')

    menus = []
    menus.append(NukeMenu(0, m))

    #### CURRENT PROBLEM: YOU ARE NOT DEALING WITH MULTIPLE GIZMOS IN A FOLDER
    # Creating submenus and assigning gizmos to them
    for x in range(0, len(gizmos)):
        gizmoFileName = gizmos[x][-1]
        gizmoName = gizmoFileName.split(".")[0]

        print("gizmoFileName: " + gizmoFileName)

        if x != len(gizmos[x])-1:
            for y in range(0, len(gizmos[x])-1):
                menus.append(NukeMenu(y+1, toolbar.addMenu(gizmos[x][y])))
                print("Added menu: " + gizmos[x][y])
        elif gizmoFileName[-4:] != ".png":
            menus[x].content.addCommand(gizmoName, f"nuke.createNode('{gizmoFileName}')")
            print("Added gizmo: " + gizmoFileName)

    return 0

if __name__=="__main__": 
    main() 
