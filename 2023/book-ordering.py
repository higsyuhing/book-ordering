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




'''
index = 0
for line in lines: 
    match = re.search(r'# (.+), # ([0-9]+), # ([0-9])', line)
    strtitle = match.group(1)
    intpagenum = int(match.group(2))
    intcategory = int(match.group(3))
    book_list.append([index, strtitle, intpagenum, intcategory])
    index += 1
    pass


# compute weights: f1, f2, wi

# compute f1, only has first 4 fields in book_list structure
def func_f1(book_list): 
    lookup = [0.2, 0.3, 0.5]
    for book in book_list: 
        intcategory = book[3] - 1
        book.append(lookup[intcategory])
        pass
    pass

func_f1(book_list)

# compute f2, only has first 5 fields in book_list structure
def func_f2(book_list): 
    tmp_1opn = [] # tmp, one over page number
    tmp_sum = 0.0
    for book in book_list: 
        intpagenum = book[2]
        tmp = 1.0/intpagenum
        tmp_1opn.append(tmp)
        tmp_sum += tmp
        pass
    index = 0
    for book in book_list: 
        tmp_res = tmp_1opn[index] / tmp_sum
        book.append(tmp_res)
        index += 1
        pass
    pass

func_f2(book_list)

# compute wi, and check point. 
for book in book_list: 
    valf1 = book[4]
    valf2 = book[5]
    weight = (valf1 + valf2) / 2
    book.append(weight) # 6
    
    # print
    strindex = str(book[0])
    strtitle = book[1]
    strpagenum = str(book[2])
    strcategory = str(book[3])
    strf1 = str(valf1)
    strf2 = str(valf2)
    strwi = str(weight)
    print("index: " + strindex + ", pn: " + strpagenum + ", c: " + strcategory + \
        ", f1 " + strf1 + ", f2 " + strf2 + ", w: " + strwi + ", title: " + strtitle)
    pass


# algorithm

# - while (not empty)
#     - compute adjusted weight: wi' = wi / sum (wi)
#     - line segment range: 1000*wi', start and end
#     - random number generate from [0, 1000)
#     - select the located segment -> selected book
#     - insert book into output list and set=set-book

result = []

bookset = range(len(book_list))

while len(bookset) > 0: 
    listindex = []
    listwia = [] # also segment range. 
    sumwia = 0.0
    
    # install info into book set
    for index in bookset: 
        listindex.append(index)
        tmpweight = book_list[index][6]
        listwia.append(tmpweight)
        sumwia += tmpweight
        pass
    # compute wi' then segment range
    for ii in range(len(listwia)): 
        wia = listwia[ii] / sumwia
        listwia[ii] = wia*1000 # segment range
        pass
    
    numrand = random.random()*1000 # get random number from [0, 1000)
    currpos = 0.0
    currindex = 0
    for currwia in listwia: 
        currpos += currwia
        if numrand < currpos: # find it. 
            result.append(listindex[currindex])
            break
        currindex += 1
        pass
    
    # delete the index from book set
    del bookset[currindex]
    pass


# print result
print("\nRandom Sequence: ")
for index in result: 
    book = book_list[index]
    # print
    strindex = str(book[0])
    strtitle = book[1]
    strpagenum = str(book[2])
    strcategory = str(book[3])
    strf1 = str(book[4])
    strf2 = str(book[5])
    strwi = str(book[6])
    print("index: " + strindex + ", pn: " + strpagenum + ", c: " + strcategory + \
        ", f1 " + strf1 + ", f2 " + strf2 + ", w: " + strwi + ", title: " + strtitle)
    pass






'''








