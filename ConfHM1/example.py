import tarfile
from io import BytesIO
import tkinter as tk

def emu():
    global path
    com = input_area.get("1.0", tk.END)[2:-1]
    print(com)
    if com == "ls":
        output_area.insert(tk.END, mainname + " " + VirtPAth[10:] + " " + com + "\n")
        with tarfile.open('home1.tar', 'a') as tar:
            for member in tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if path == np:
                    output_area.insert(tk.END, last + (" " * 2))
        output_area.insert(tk.END, "\n")
    elif com.startswith("exit"):
        exit()
    elif com.startswith("cd "):
        output_area.insert(tk.END, mainname + " " + VirtPAth[10:] + " " + com + "\n")
        parts = com.split(" ")
        path = parts[1].split("/")
        path = [i for i in path if i != ""]
    elif com.startswith("cp "):
        output_area.insert(tk.END, mainname + " " + VirtPAth[10:] + " " + com + "\n")
        with tarfile.open('home1.tar', 'r') as tar:
            parts = com.split(" ")
            np = com.split(" ")[2]
            name = com.split(" ")[1]
            name= '/'.join(path + [name])
            bytes = tar.extractfile(name).read()
        with tarfile.open('home1.tar', 'a') as tar:
            io = BytesIO()
            io.write(bytes)
            io.seek(0)
            info = tarfile.TarInfo(name=np)
            info.size=len(bytes)
            tar.addfile(tarinfo=info, fileobj=io)
    elif com.startswith("clear"):
        output_area.delete('1.0', tk.END)
    input_area.delete("1.0", tk.END)
    input_area.insert(tk.END, "$ ")


path = []
root = tk.Tk()
root.title("GUI")
output_area = tk.Text(root, height=20, width=100)
output_area.pack(pady=10)
input_area = tk.Text(root, height=5, width=100)
input_area.pack(pady=10)
copy_button = tk.Button(root, text="Enter", command=emu)
copy_button.pack(pady=5)
input_area.insert(tk.END, "$ ")

with open("config.ini",'r', encoding='UTF-8') as f:
    line = f.read()
    line = line.splitlines()
    for name in line:
        if(name.startswith('Name = ')):
            mainname = name.replace("Name = ", "", 1)
        elif(name.startswith('VirtPath = ')):
            VirtPAth = name.replace("VirtPath = ", "", 1)
            VirtPAth = name.replace("\\", "\\\\")
        elif(name.startswith('ScripPath = ')):
             ScripPath = name.replace("ScripPath = ", "", 1)

with open(ScripPath, 'r') as file:
    script = file.readlines()
    for cmd in script:
        input_area.insert(tk.END, cmd.strip())
        emu()

root.mainloop()
