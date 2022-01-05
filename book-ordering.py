#!/bin/python

import re
import random

'''
random book ordering generator, for coffee chat. 
MW 2022.01.05

input data format: 
    "# $(book title), # $(page number), # $(category)

current category: 
    $(1) member recommended
    $(2) get 2 tickets
    $(3) get 3 tickets

ordering weight, 2 factors: 
    - f1, category: $(3)=50% > $(2)=30% > $(1)=20%
    - f2, page number: 1/$(page num) / sum( 1/$(page num) )
        a book with more pages has less chance ordering ahead. 
    = f1, f2 50% weight each

algorithm: 
- compute each book's overall weight: w=0.5*f1+0.5*f2
- while (not empty)
    - compute adjusted weight: wi' = wi / sum (wi)
    - line segment range: 1000*wi', start and end
    - random number generate from [0, 1000)
    - select the located segment -> selected book
    - insert book into output list and set=set-book

book_list structure: 
    [index, title, page number, category, f1, f2, wi]
'''

# read data, construct book_list basic info
fd = open("book-data.txt", "r")
lines = fd.readlines()
fd.close()

book_list = []

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
'''
- while (not empty)
    - compute adjusted weight: wi' = wi / sum (wi)
    - line segment range: 1000*wi', start and end
    - random number generate from [0, 1000)
    - select the located segment -> selected book
    - insert book into output list and set=set-book
'''
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















