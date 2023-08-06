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
def removeforlder(foldername):
    return os.system("rmdir "+ foldername)
def runpython(file):
    os.system("python3 " + file)
def runconsole(command):
    os.system(command)
