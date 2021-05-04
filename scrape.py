#!/usr/local/bin/python3

import sys
import urllib3.request
from urllib.request import urlopen
import re
import unicodedata
from bs4 import BeautifulSoup
import json

courses = dict()

# retrive html code from given url
def read_url(url):
    with urlopen(url) as fp:
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
    return mystr

# get all target links on a page
def get_pgs(dir_url):
    direc = read_url(dir_url)
    soup = BeautifulSoup(direc, 'html.parser')
    for tr in soup.find_all('a',target="_blank",href=re.compile("preview_course_nopop.php")):
        # courses[unicodedata.normalize("NFKD", tr.string)] = tr.get("href")
        link = 'http://catalog.hunter.cuny.edu/{}'.format(tr.get("href"))
        # print("\n\n\nhttp://catalog.hunter.cuny.edu/{}\n".format(link))
        course_desc = BeautifulSoup(read_url(link), 'html.parser')
        for td in course_desc.find_all('td',attrs={"class":"block_content"}):
            info = [i for i in td.p.strings if i.strip() != ""]
            #print(info)
            name = info[0].split("-", 1)
            dct = { 
                'name': name[1].strip(),
                'link': link,
                'full':info
            }
            if len(info) == 1:
                courses[name[0].strip()] = dct
                continue 

            dct['description'] = ""
            dct['fulfills'] = dict()

            exclude = [0]
            prereq_ind = None
            for i in range(len(info)):
                if " hr" in info[i] and bool(re.search(r'\d', info[i][0])): 
                    dct['hours'] = info[i]
                    exclude.append(i)
                if " cr" in info[i] and bool(re.search(r'\d', info[i][0])):
                    dct['credits'] = info[i]
                    exclude.append(i)
                if "Print-Friendly" in info[i] or "Back to Top" in info[i] or info[i] == "":
                    exclude.append(i)
                if info[i] == 'prereq:':
                    dct['prereq'] = info[i+1]
                    prereq_ind = i
                    exclude.append(i)
                    exclude.append(i + 1)
                if 'prereq: ' in info[i]:
                    dct['prereq'] = info[i]
                    prereq_ind = i
                    exclude.append(i)
                if 'Hunter Core' == info[i]:
                    dct['fulfills'][info[i]] = info[i+1]
                    exclude.append(i)
                    exclude.append(i+1)
                if 'Pluralism and Diversity' == info[i]:
                    dct['fulfills'][info[i]] = info[i+1]
                    exclude.append(i)
                    exclude.append(i+1)
                if 'GER' == info[i].split(" ",1)[0]:
                    exclude.append(i)
                    if len(info[i].split(" ",1)) > 1: 
                        dct['fulfills'][info[i].split(" ",1)[0]] = info[i].split(" ", 1)[1]
                    elif i+1 < len(info):
                        dct['fulfills'][info[i]] = info[i+1]
                        exclude.append(i+1)

            excl = [len(i) for c, i in enumerate(info) if c not in exclude]
            longest = max(excl) if len(excl) > 0 else 0
            longest_pos = prereq_ind if prereq_ind else len(info)-1
            for i in range(len(info)):
                if len(info[i]) == longest:
                    dct['description'] = info[i]
                    longest_pos = i
                    #exclude.append(i)
            # etc = info[1:longest_pos]
            etc = [i for c, i in enumerate(info) if c not in exclude]

            dct['etc'] = etc #dict(zip(etc[::2],etc[1::2]))
            #if (dct['etc'] == [] and dct['fulfills'] != dict()) or
            '''
            if dct['description'] == "":
                print([(i,c) for c, i in enumerate(info) if c not in exclude])
                for i in info:
                    print(i)
                print("")
                print(dct['description'])
                print(dct)
                print("")
            '''
            if "(W)" in info[0]:
                dct['fulfills']['WI'] = True

            #print(dct)
            courses[name[0].strip()] = dct


for start_num in range(1, 26):
    print("pg ", start_num)
    #dir_url = "http://catalog.hunter.cuny.edu/content.php?catoid=39&catoid=39&navoid=11821&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=" + str(start_num) + "#acalog_template_course_filter"
    dir_url = "http://catalog.hunter.cuny.edu/content.php?catoid=43&catoid=43&navoid=13946&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=" + str(start_num) + "#acalog_template_course_filter"
    get_pgs(dir_url)
    #print(courses)
    with open('data/courses.json', 'w') as outfile:
        json.dump(courses, outfile)

#print(courses)

#with open('data/courses.json', 'w') as outfile:
#    json.dump(courses, outfile)

