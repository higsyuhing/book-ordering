#!/bin/python

import re
from bs4 import BeautifulSoup
import requests


'''
book select
MW 2023.01.02

just re-generate them into a google sheet format.. but
some books are selected in multiple tags, I need to highlight them. 

data structure: 

book_group: list of: 
    tag, book info

then a new list: 
tag='multiple', book info='name / author \t tag;tag;..

output: a txt file: 

multiple tags
name\t\tauthor\t\ttags

tag
name\t\tauthor

'''

def getlink(name): 
    search = name + ' douban'
    url = 'https://www.google.com/search'

    headers = {
        'Accept' : '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {'q': search}

    content = requests.get(url, headers = headers, params = parameters).text
    soup = BeautifulSoup(content, 'html.parser')

    search = soup.find(id = 'search')
    first_link = search.find('a')

    ret = first_link['href']
    print("search " + str(name) + ": " + ret)
    return ret



# read data, construct book_list basic info
fd = open("book-data.txt", "r")
lines = fd.readlines()
fd.close()

book_group = []
book_dict = {}

tag = ""
for line in lines: 
    match = re.search(r'^#(.+)', line)
    if match: 
        tag = match.group(1)
        book_group.append([tag, []])
        continue
    match = re.search(r'^\d+\.(.+)\|(.+)', line)
    if match: 
        name = match.group(1)
        author = match.group(2)
        info = [name, author, getlink(name)]
        book_group[-1][1].append(info)
        # if name not in book_dict: 
        #     book_dict[name] = [0, author, tag]
        #     pass
        # else: 
        #     book_dict[name][0] = 1
        #     book_dict[name][2] = book_dict[name][2] + "; " + tag
        # pass
    pass

print("\n\n")
for groupinfo in book_group: 
    print("\n" + str(groupinfo[0]))
    for info in groupinfo[1]: 
        print(str(info[0]) + "\t\t" + str(info[1]) + "\t\t" + str(info[2]))
        pass
    pass

# for name in book_dict: 
#     value = book_dict[name]
#     if value[0] == 1: 
#         print(str(name) + "\t\t" + str(value[1]) + "\t\t" + str(value[2]))
#         pass
#     pass






