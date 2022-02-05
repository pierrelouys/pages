import xml.etree.ElementTree as ET
import os, sys, re

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

search_terms = ["PlayStation (", "Playstation (", "PS1", "PSX"]
# search_terms = ["PlayStation 2 (", "Playstation 2 (", "PS2"]
# search_terms = ["GameCube", "Gamecube"]

# https://www.arcade-history.com/index.php?page=download
root = ET.parse('history.xml').getroot()
for entry in root:
    for child in entry: 
        if child.find("system") != None:
            rom_name = (child.find("system").attrib.get("name"))  
        # if child.text.find("PlayStation CD published") != -1:
            # continue
            
        search_matches = 0
        for search_term in search_terms:
            if child.text.find(search_term) != -1:
                search_matches += 1
        if search_matches < 1:
            continue
            
        child_lines = child.text.split("\n")
        p = re.compile(r'tation\s\([^\)]+\)\s\"([^"]+)\"')
        
        release = ""
        for line in child_lines:
            if p.search(line) != None:
                release = " (in " + p.search(line).group(1) + ")"
                
        # print("http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=" + rom_name, child.text.split("\n")[0], child.text.split("\n")[1], child.text.split("\n")[2], child.text.split("\n")[3])
        title = child.text.split("\n")[3]
        if title == "":
            title = child.text.split("\n")[2]
        if title == "":
            title = child.text.split("\n")[1]
        if title == "":
            title = child.text.split("\n")[0]
        print("- [" + title + "]" + "(" + "http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=" + rom_name + ")" + release)
