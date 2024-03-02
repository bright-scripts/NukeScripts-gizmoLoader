# Gizmo Loader for Nuke

## Setup:

1) Copy the contents of `init.py` into your `init.py` in your `.nuke` folder. (If you don't have a `init.py` in your `.nuke`, just copy in this one)
2) Set up plugin folder and path:
   
   - Copy the `gizmoLoaderPlugin` folder into your `.nuke` folder
   
   - Open the `menu.py` file and replace the text in the sixth line with the path to your `.nuke` directory. (this is a janky solution that will be changed in the next patch(most likely))
   (i.e.: `dotNukePath = "C:/Users/user/.nuke"`)
4) Create a folder named `gizmoLoader` in your `.nuke/ToolSets` folder
5) Copy any gizmo files, you'd like the script to auto load, into the `.nuke/ToolSets/gizmoLoader` folder
    - You can organize them into folder structures inside the `.nuke/ToolSets/gizmoLoader` directory and the plugin will use that for the menu structure inside Nuke
