#!/usr/bin/python

import sys, os

#print(os.listdir('.'))

def descriptions(): 
    # scraped course data -- scrape.py
    # course id, name of course, link
    fin = open(os.getcwd() + "/data/" + "courses.txt")
    course_raw = [i.replace("-","**").split("*") for i in fin.read().split("\n") if i != ""]
    course_desc = {i[0].strip():[i[-2].strip(), "http://catalog.hunter.cuny.edu/" + i[-1]] for i in course_raw}
    fin.close()
    return course_desc


def courses_fulfill():
    files = [f for f in os.listdir(os.getcwd() + '/data') if f != "classes.py" and f != "scrape.py" and f!= "courses.txt" and f[-4:] == ".txt"] 
    names = [f[0:-4] for f in files] 
    dicts = []

    print(files)

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

def fulfillments(cl_ind, d):
    fulfills = {i:0 for i in cl_ind}
    reqs = {i:[] for i in cl_ind}
    reqs_real = {i:set() for i in cl_ind}
    lengths = {1 : 0, 2 : 0, 3 : 0}

    # number of and which specific requirements a class fulfills
    for i in d: 
        for n in d[i]:
           #fulfills[n] += 1
           reqs[n].append(i)
           reqs_real[n].add(i.split('_')[0])
           fulfills[n] = len(reqs_real[n])

    # find the number of classes the fulfill X requirements
    for i in fulfills: 
        lengths[fulfills[i]] += 1
    return fulfills, reqs 

def seek(fulfills, reqs, course_desc, n, hardness, out, comp=">="):
    print(comp)
    if comp == ">=":
        good = {i : reqs[i] for i in fulfills if fulfills[i] >= int(n)}
    if comp == "==":
        good = {i : reqs[i] for i in fulfills if fulfills[i] == int(n)}

    alph = sorted(good.keys())
    bb = ""

    for i in alph: 
        l = i.split(" ")
        if int(l[1][0]) < int(hardness): 
            c = ""
            l = "\n"
            alt_name_1 = i[:-2] + "00"
            alt_name_2 = i[:-2] + "XX"
            if course_desc.get(i):
                c += " - " + course_desc.get(i)[0]
                l += course_desc.get(i)[1] + "\n"
            elif i != alt_name_1 and course_desc.get(alt_name_1):
                c += " (" + alt_name_1 + ") - " + course_desc.get(alt_name_1)[0]
                l += course_desc.get(alt_name_1)[1] + "\n"
            elif i != alt_name_2 and course_desc.get(alt_name_2):
                c += " (" + alt_name_2 + ") - " + course_desc.get(alt_name_2)[0]
                l += course_desc.get(alt_name_2)[1] + "\n"
            bb += i + c + "\t" + str(good[i]) + l + "\n" 
            print(i + c + "\t" + str(good[i]) + l)

    f = open(out, "w")
    f.write(bb)
    f.close()


if __name__ == "__main__":
    desc = descriptions()
    ci, dct = courses_fulfill()
    fulfills, reqs = fulfillments(ci, dct)
    if len(sys.argv) > 4:
        seek(fulfills, reqs, desc, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        seek(fulfills, reqs, desc, sys.argv[1], sys.argv[2], sys.argv[3])
    print(sys.argv)
