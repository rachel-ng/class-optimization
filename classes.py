#!/usr/bin/python

import sys, os, copy
import argparse
import json


#print(os.listdir('.'))

def descriptions(): 
    # scraped course data -- scrape.py
    # course id, name of course, link
    fin = open(os.getcwd() + "/data/" + "courses.txt")
    course_raw = [i.replace("-","*",1).split("*") for i in fin.read().split("\n") if i != ""]
    course_desc = {i[0].split("(")[0].strip():[i[-2].strip(), "http://catalog.hunter.cuny.edu/" + i[-1]] for i in course_raw}
    fin.close()
    return course_desc


def descriptions_json():
    with open(os.getcwd() + "/data/" + "courses.json") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data 


def courses_fulfill():
    files = [f for f in os.listdir(os.getcwd() + '/data') if f != "classes.py" and f != "scrape.py" and f!= "courses.txt" and f[-4:] == ".txt"] 
    names = [f[0:-4] for f in files] 
    dicts = []

    print(files)
    print("\n\n")

    cl_ind = set()
    for f in files:
        fin = open(os.getcwd() + '/data/' + f,"r")

        # clean up data 
        clean_1 = [i.replace(" ","").split("|") for i in fin.read().split("\n") if i != ""]
        clean_2 = [[i[0] + " " + k for k in i[1].split("or") if k != ""] for i in clean_1]

        # flatten list, turn into set
        cat_classes = set(item for sublist in clean_2 for item in sublist)
        
        dicts.append(cat_classes)
        cl_ind.update(cat_classes)
        
        fin.close()

    # requirements: courses that fulfill it 
    d = dict(zip(names,dicts))

    return cl_ind, d


def courses_exclude():
    fin = open(os.getcwd() + '/user/taken.txt',"r")
    classes = [i for i in fin.read().split("\n") if i!= ""] 
    return classes

def fulfillments(cl_ind, d, course_desc, excl):
    fulfills = {i:0 for i in cl_ind}
    reqs = {i:[] for i in cl_ind}
    reqs_real = {i:set() for i in cl_ind}
    lengths = {0 : 0, 1 : 0, 2 : 0, 3 : 0}
    wi = set()
    
    # number of and which specific requirements a class fulfills
    for i in d: 
        for n in d[i]:
            #fulfills[n] += 1
            if i not in excl: 
                reqs[n].append(i)
                reqs_real[n].add(i.split('plurdiv_')[0])
            if course_desc.get(n):
                if len(course_desc.get(n)['name'].split("(W)")) > 1:
                    wi.add(n)
            fulfills[n] = len(reqs_real[n])
                # find the number of classes the fulfill X requirements
    for i in fulfills: 
        lengths[fulfills[i]] += 1
  
    return fulfills, {i:(reqs[i]+["WI"] if (i in wi) else reqs[i]) for i in reqs}, wi


def seek(fulfills, reqs, wi, course_desc, n, hardness, out, comp, w, pref):
    ok = {}

    if comp == ">=" or comp == None:
        if w == "Y" or w == "y":
            ok = {i : reqs[i] for i in fulfills if fulfills[i] >= int(n) and "WI" in reqs[i]}
        elif w == "N" or w == "n":
            ok = {i : reqs[i] for i in fulfills if fulfills[i] >= int(n) and "WI" not in reqs[i]}
        else: 
            ok = {i : reqs[i] for i in fulfills if fulfills[i] >= int(n)}

    if comp == "==":
        if w == "Y" or w == "y":
            ok = {i : reqs[i] for i in fulfills if fulfills[i] == int(n) and "WI" in reqs[i]}
        elif w == "N" or w == "n":
            ok = {i : reqs[i] for i in fulfills if fulfills[i] == int(n) and "WI" not in reqs[i]}
        else:
            ok = {i : reqs[i] for i in fulfills if fulfills[i] == int(n)}

    '''
    if fulfilled != "-":
        fin = open("user/" + fulfilled, "r")
        completed = [i for i in fin.read().split("\n") if i != ""]
        fin.close()
        
        print(completed)
        
        good = copy.deepcopy(ok) 
        for i in ok:
            print(good[i])
            for n in completed: 
                if n in ok[i]:
                    good.pop(i, None)
                    break
            print(good[i])
            print("")
    else:
    '''    

    good = copy.deepcopy(ok) 
    
    alph = sorted(good.keys())
    bb = ""
    bb += "python classes.py {} {} {} {} {}\n\n".format(n, hardness, out, comp, w)
    num = 0
    for i in alph: 
        l = i.split(" ")
        if int(l[1][0]) < int(hardness): 
            if pref != "" and pref in good[i]: 
                num += 1
                c = ""
                l = "\n"
                alt_name_1 = i[:-2] + "00"
                alt_name_2 = i[:-2] + "XX"
                if course_desc.get(i):
                    cdct = course_desc.get(i)
                    c += " - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"
                    #l += str(cdct['fulfills']) + "\n\n"
                    #l += str(cdct) + "\n"
                elif i != alt_name_1 and course_desc.get(alt_name_1):
                    cdct = course_desc.get(alt_name_1)
                    c += " (" + alt_name_1 + ") - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"
                elif i != alt_name_2 and course_desc.get(alt_name_2):
                    cdct = course_desc.get(alt_name_2)
                    c += " (" + alt_name_2 + ") - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"

                if (course_desc.get(i)):
                    bb += i + c + "\t" + str(good[i]) + l + "\n" 
                    print(i + c + "\t" + str(good[i]) + l + "\n")
                else:
                    bb += i + "\nunable to find more info\n" 
                    print(i + "\nunable to find more info\n") 

            elif pref == "": 
                num += 1
                c = ""
                l = "\n"
                alt_name_1 = i[:-2] + "00"
                alt_name_2 = i[:-2] + "XX"
                if course_desc.get(i):
                    cdct = course_desc.get(i)
                    c += " - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"
                    #l += "{}\n\n{}\n".format(cdct['link'],cdct['description'])
                elif i != alt_name_1 and course_desc.get(alt_name_1):
                    cdct = course_desc.get(alt_name_1)
                    c += " (" + alt_name_1 + ") - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"
                elif i != alt_name_2 and course_desc.get(alt_name_2):
                    cdct = course_desc.get(alt_name_2)
                    c += " (" + alt_name_2 + ") - " + cdct['name']
                    l += cdct['link'] + "\n\n" 
                    l += cdct['description'] + "\n"

                if (course_desc.get(i)):
                    bb += i + c + "\t" + str(good[i]) + l + "\n" 
                    print(i + c + "\t" + str(good[i]) + l + "\n")
                else:
                    bb += i + "\nunable to find more info\n" 
                    print(i + "\nunable to find more info\n") 

    print("{} classes found".format(num))
    f = open("output/" + out, "w")
    f.write(bb.encode("utf-8"))
    f.close()


def parse (): 
    parser = argparse.ArgumentParser(description='finding courses that fulfill more requirements')
    parser.add_argument('-f','--fulfill', default=2, 
        help='requirements you want classes to fulfill, default=2'
    )
    parser.add_argument('-l','--level', default=3,
        help='hardness of classes (up to X00 level), default=3'
    )
    parser.add_argument('-o','--output', default="out.txt",
        help='output file, default = "output/out.txt"'
    )
    parser.add_argument('-c', choices=[">=","==",[]], 
        help='comparison used for requirements fulfilled,  default=">="'
    )
    parser.add_argument('--wi', choices=["y","Y","n","N",[]],
        help='writing intensive classes, default shows all classes'
    )
    parser.add_argument('-p','--pref', default="",
        help='preferred requirement, default = ""'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse()
    print(args)
    #desc = descriptions()
    desc = descriptions_json()
    ci, dct = courses_fulfill()
    excl = courses_exclude()
    fulfills, reqs, wi = fulfillments(ci, dct, desc, excl)
    seek(fulfills, reqs, wi, desc, int(args.fulfill), int(args.level), args.output, args.c, args.wi, args.pref)


