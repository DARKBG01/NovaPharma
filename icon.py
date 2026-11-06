import glob
import os


os.chdir("Assets/")
os.remove("Icon.qrc") if os.path.exists("Icon.qrc") else None
with open("Icon.qrc","a") as file:
    print(glob.glob("Icons/*"))
    file.write("<RCC>\n")
    file.write("    <qresource prefix='Icon'> \n")
    for i in glob.glob("Icons/*"):
        print(i)
        if not ("." in i):
            continue
        file.write(f"        <file>{i}</file>\n")
    file.write("     </qresource>\n")
    file.write("</RCC>")
    
    #os.system("pyside6-rcc Icon.qrc -o ../Icon_rc.py")
    #file.write("    <qresource prefix='feather'> \n")