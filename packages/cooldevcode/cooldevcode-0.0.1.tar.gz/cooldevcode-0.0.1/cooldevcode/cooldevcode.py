from tkinter import *
import string as s
alphabets = s.ascii_uppercase + s.ascii_lowercase
alphabets2 = "ZAYBXCWDVEUFTGSHRIQJPKOLNMzaybxcwdveuftgshriqjpkolnm"
numbers = "0123456789"
special_cirectors = """./\π#~<>,¬`!£$^%&*()-=_+[]{}:;@'\" ?|"""
v1 = alphabets + numbers + special_cirectors
v2 = alphabets2 + numbers + special_cirectors
ss = ("sans-serif", 16)

is_activated = False

dict2 = {}
dict1 = {}

def push_to_dict(text, dict_name):
    for i in text:
        if text.index(i) <= 9:
            dict_name[i] = "0" + str(text.index(i))
        else:
            dict_name[i] = str(text.index(i))

def opposite_dict(current, res):
    for i in current:
        res[current[i]]=i

def print_list(list_name):
    for i in list_name:
        print(i)

def print_dict(dict_name):
    for i in dict_name:
        print(i + " : " + str(dict_name[i]))
    
def encode(text):
    if is_activated:
        res = ""
        for i in text:
            if i == '\n':
                res = res + "99"
            elif i == '\t':
                res = res + "98"
            elif i == '\r':
                res = res + "97"
            else:
                res = res + dict1[i]
        return res
    else:
        print("Please activate first to use COOLCODE.")
        
def decode(code):
    if is_activated:
        turn = False
        res= ""
        
        #current code
        cc = ""
        for i in code:
            if turn:
                cc = cc + str(i)
                if cc == "99":
                    res = res + '\n'
                    turn = False
                elif cc == "98":
                    res = res + '\t'
                    turn = False
                elif cc == "97":
                    res = res + '\r'
                    turn = False
                else:
                    res = res + dict2[cc]
                    turn = False
            else:
                cc = ""
                cc = str(i)
                turn = True
        return res
    else:
        print("Please activate first to use COOLCODE.")

def read_file(name):
    with open(name, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(name, text):
    with open(name, 'w') as file:
        file.write(text)

def activate(v):
    global is_activated 
    if v == "v1":
        push_to_dict(v1, dict1)
        opposite_dict(dict1, dict2)
        is_activated = True
    elif v == "v2":
        push_to_dict(v2, dict1)
        opposite_dict(dict1, dict2)
        is_activated = True
    else:
        print(f"Your requested version {v} is not an existed version.")

def encode_file(f):
    with open(f, 'r') as file:
        text = file.read()
        write_file(f+".enc", encode(text))

def decode_file(f):
    with open(f, 'r') as file:
        text = file.read()
        write_file(f+".decoded", decode(text))
