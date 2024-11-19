import requests
from bs4 import BeautifulSoup

from plantuml import PlantUML

def deps(name):
    url = "https://pkgs.alpinelinux.org" + name
    html = requests.get(url).text
    parsed_html = BeautifulSoup(html, features= "html.parser")
    for details in parsed_html.body.find_all("details"): 
        text:str = details.find("summary").text
        if text.startswith("Depends",0):
            break
    array = []
    source = name.split("/")[-1]
    for a in details.find_all("a"):
      if("None" in a):
        continue
      href = a["href"]
      dest = href.split("/")[-1]
      array.append([source,dest])
      print(source + "  ->  " + dest)
      array += deps(href)
    return array

def plantuml(deps):
  text = "@startuml\n"
  for src, dest in deps:
      text += f'"{src}" --> [ ] "{dest}"\n'
  text += "@enduml"
  return text

def getting_image(text,outputpath,path):
    plantuml_url = path
    plantuml = PlantUML(url=plantuml_url)
    image = plantuml.processes(text)
    with open(outputpath, "wb") as file:
      file.write(image)

with open("config.xml", encoding = "UTF-8") as f:
  line = f.read()
  line = line.splitlines()
  for name in line:
    if(name.startswith('path = ')):
      path = name.replace("path = ", "", 1)
    elif(name.startswith('OutputPath = ')):
       OutputPath = name.replace("OutputPath = ", "", 1)
    elif(name.startswith('package = ')):
       pack = name.replace("package = ", "", 1)


getting_image(plantuml(deps(pack)),OutputPath, path)