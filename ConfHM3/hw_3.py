def text(file):
    with open(file + ".yaml", 'r') as f:
        line = f.read() 
        const_dict = {}
        line = line.splitlines()
        for i in range(len(line)):
            if ("constants:" in line[i]):
                for y in range(i, len(line)):
                    if (line[y].strip().startswith("- var")):
                        name = line[y].strip().split(" ")[2]
                        val = int(line[y].strip().split(" ")[3][:-1])
                        const_dict[name] = val
                print(const_dict)
            if("dictionaries:" in line[i]):
                dict = {}
                for y in range(i+1, len(line)):
                    if(line[y].strip().startswith("-")):
                        name = line[y].strip().split(" ")[1][:-1]
                    elif(line[y].strip().split(" ")[0].endswith(":") and not line[y].strip().startswith("-")):
                        key = line[y].strip().split(" ")[0][:-1]
                        val = line[y].strip().split(" ")[1]
                        dict.setdefault(name, []).append({key:val})
                print(dict)    
    

text("test")
