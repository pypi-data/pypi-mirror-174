import os

def message(message):
    return print(message)
def add(num1, num2):
    return num1 + num2
def subtract(num1, num2):
    return num1 - num2
def multiply(num1, num2):
    return num1 * num2
def divide(num1, num2):
    return num1 / num2
def createfolder(foldername):
    return os.system("mkdir " + foldername)
def removefolder(foldername):
    return os.system("rmdir "+ foldername)
def runpython(file):
    os.system("python3 " + file)
def runconsole(command):
    os.system(command)
def halloween():
    halloweenprint = True
    print("Happy Halloween :)))))")
    print("Here type anything you want :): ")
    print("If you want to quit the program just type 'exit', 'stop', 'quit'!")
    while halloweenprint == True:
        answer = input()
        print(answer)
        if answer == "quit" or answer == "exit" or answer == "stop":
            print("Bye! Have a nice halloween day! :D")
            halloweenprint = False
            break
