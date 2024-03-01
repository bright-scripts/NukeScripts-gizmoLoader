import nuke
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
        this = []
        for y in x:
            this.append(f"{y.isDirectory} | {y.content}")
        # print(f"[{x}] - {this}")

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
        depth = 0
        for y in range(0, len(gizmos[x])):

            if gizmos[x][y].isDirectory:
                if len(gizmos[x][y].content) != 0:
                    
                    thisMenu=0

                    for z in range(0, len(menus)):
                        if len(gizmos[x][y].content) >= 2:
                            if menus[z].name() == gizmos[x][y].content[-2]:
                                thisMenu = z
                                print("!!! Found this: " + menus[z].name())
                                break
                    
                    print(f"menu len: {len(menus)} | thisMenu: {thisMenu}")
                    menus.append(menus[thisMenu].addMenu(gizmos[x][y].content[-1], index = 0))
                    # depth = len(gizmos[x][y].content)-1
                    # menus.append(menus[depth].addMenu(gizmos[x][y].content[-1], index = 0))
                    print(f"Menu created: {gizmos[x][y].content[-1]} -> {menus[-1].name()} in **{menus[thisMenu].name()}**")
                    
                    # print(f"FOLDER I&N: len(m): {len(menus)} d:[{depth}] x:[{x}] y:[{y}] - {gizmos[x][y].content[-1]}\n")


            else:
                thisMenu = x
                for z in range(0, len(menus)):
                    if len(gizmos[x][0].content) != 0:
                        if menus[z].name() == gizmos[x][0].content[-1]:
                            thisMenu = z
                            print("Found this: " + menus[z].name())
                            break

                menus[thisMenu].addCommand(gizmos[x][y].content.split('.')[0], f"nuke.createNode({gizmos[x][y].content})")
                print(f"len(m): {len(menus)} d:[{depth}] x:[{x}] y:[{y}] - Added **{gizmos[x][y].content}** to **{menus[thisMenu].name()}**")
        print("\n---")


    return 0

if __name__=="__main__": 
    main() 
