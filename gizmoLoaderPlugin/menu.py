import nuke
import os
from inspect import getframeinfo, currentframe

def main(): 

    #Finding .nuke folder based on the location of this very .py script runs from
    filename = getframeinfo(currentframe()).filename

    if filename.find(".nuke") == -1:
        print("# gizmoLoaderPlugin:\n\tYour .nuke folder couldn't be found.\n\tPlease reference the README.md file on github to see where to paste files from the repo for it to work.\n\tIf you are sure you are doing things properly and you still get this error please contact the dev on discord: @mellow_moth")
        exit (code="ERROR: gizmoLoaderPlugin: .nuke/ not found")

    dotNukePath = os.path.dirname(os.path.abspath(filename))[0:filename.find(".nuke")+5].replace("\\", "/")
    path = dotNukePath+"/ToolSets/gizmoLoader"

    # Creating the gizmoLoader folder if it doesn't already exist
    if not os.path.isdir(path):
        os.makedirs(path)
        print("##############################\nNO FOLDER NAMED \"gizmoLoader\" HAS BEEN FOUND, creating it now.\n##############################")

    gizmos = discover(path)

    for x in gizmos:
        this = []
        for y in x:
            this.append(f"{y.isDirectory} | {y.content}")

    build(path, gizmos)

    ### END OF main() ###

# Creating a class for buildanizing menus
class NukeMenu:
    def __init__(self, level, content):
        self.level = level
        self.content = content
    def __str__(self):
        return f"level: {self.level} | content: {self.content})"

# Creating a class for buildanizing items
class NukeItem:
    def __init__(self, isDirectory, content):
        self.isDirectory = isDirectory
        self.content = content
    def __str__(self):
        return f"isDirectory: {self.isDirectory} | content: {self.content})"

# Function responsible for discovering gizmos
def discover(fromHere):
    # Discovering directories and files in `fromHere` folder
    discovery = os.walk(top=fromHere)


    # Formatting discovery info into menus
    gizmos = []

    for x in discovery:
        # The line below replaces "/" found in windows' path format with "\", that python (and basically everything else?) uses.
        tempPath = x[0].replace("/", "\\").split("\\")
        items = []
        items.append(NukeItem(True, tempPath[tempPath.index("gizmoLoader")+1:]) )

        for y in x[2]:
            items.append(NukeItem(False, y))

        gizmos.append(items)

    return gizmos
    ### END OF discover() ###

# Fonction responsible for building gizmo toolbar menus
def build(path, gizmos):
    # Add PluginPaths to tools and icons
    nuke.pluginAddPath(f"{path}")

    # Create gizmoLoader Menu
    toolbar = nuke.menu('Nodes')
    m = toolbar.addMenu('GizmoLoader')

    menus = []
    menus.append(m)

    for x in range(0, len(gizmos)):
        for y in range(0, len(gizmos[x])):

            if gizmos[x][y].isDirectory:
                if len(gizmos[x][y].content) != 0:
                    
                    thisMenu=0

                    for z in range(0, len(menus)):
                        if len(gizmos[x][y].content) >= 2:
                            if menus[z].name() == gizmos[x][y].content[-2]:
                                thisMenu = z
                                break
                    
                    menus.append(menus[thisMenu].addMenu(gizmos[x][y].content[-1], index = 0))


            else:
                thisMenu = x
                for z in range(0, len(menus)):
                    if len(gizmos[x][0].content) != 0:
                        if menus[z].name() == gizmos[x][0].content[-1]:
                            thisMenu = z
                            break

                menus[thisMenu].addCommand(gizmos[x][y].content.split('.')[0], f"nuke.createNode('{gizmos[x][y].content}')")


    return 0

if __name__=="__main__": 
    main() 
