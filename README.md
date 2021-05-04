# class-optimization

<sup>now with a proper CLI!</sup>

`last scraped: 05/04/2021`  
~`last scraped: 08/12/2020 20:54:32`~   
~`last scraped: 05/04/2020 21:35:36`~ 

***NOTE**&nbsp;&nbsp;&nbsp; not all classes are available at all times* 

&nbsp; 



## terminal usage

```
(venv) $ python classes.py [-h] -f FULFILL [-l LEVEL] [-o OUTPUT] [-c {>=,==,}] [--wi {y,Y,n,N,}]

finding courses that fulfill more requirements

optional arguments:
  -h, --help            show this help message and exit
  -f FULFILL, --fulfill FULFILL
                        requirements you want classes to fulfill, default=2
  -l LEVEL, --level LEVEL
                        hardness of classes (up to X00 level), default=3
  -o OUTPUT, --output OUTPUT
                        output file, default = "output/out.txt"
  -c {>=,==,[]}         comparison used for requirements fulfilled,
                        default=">="
  --wi {y,Y,n,N,[]}     writing intensive classes, default shows all classes
```

```

CODE 10100 - Not A Real Class	['requirements', 'it', 'fulfills']
http://catalog.hunter.cuny.edu/preview_course_nopop.php?catoid=LINK&coid=TO_COURSE_DESCRIPTION

GERMN 24100 - German Fairy Tales in Translation (W)	['fcc_creative', 'plurdiv_d', 'WI']
http://catalog.hunter.cuny.edu/preview_course_nopop.php?catoid=39&coid=108730
 
```

please also look at the ***[requirements fulfilled](#requirements-fulfilled)*** and ***[scraping courses](#scraping-courses)*** sections as well for more accurate info on your situation and on the courses! 

<sub>you will need `bs4` `(beautifulsoup4)` for scraping course data</sub>  
<sup>if you decide to do so, there are [more detailed installation instructions below &or;](#installation)</sup>

<sup>[some examples of terminal usage below &or;](#examples)<sup>



#### requirements fulfilled

\# of requirements the classes fulfill  
<sub>*can be adjusted with [comparison (optional)](#comparison-optional)*</sub>

default: `2`

**NOTE**
- does not include [writing intensives](#writing-intensive-optional)
- *you can not "double dip" with requirements e.g.*

  ```
  SPAN 26900 - Spanish American Women’s Literature and Cinema (W)    ['plurdiv_a', 'plurdiv_c', 'WI']
  http://catalog.hunter.cuny.edu/preview_course_nopop.php?catoid=39&coid=109908
  ```
  
  this "fulfills" `plurdiv_a` and `plurdiv_c` and it is a writing intensive class  
  *but it only fulfills **1 (one)** of the **plurdiv (pluralism and diversity) requirements**, **not both***


#### level

default: `3` (max 300 level)

*will not go above the level you put e.g.* `4` will give you all classes **below** 400-level  
<sub>*not affected by the [comparison (optional)](#comparison-optional) used*</sub>

100-, 200-level courses — lower div courses 

300-, 400-level courses — upper div courses 

500-, 600-, 700-level courses — graduate courses


#### output file

default: `out.txt` 

writes to `output/file_name.txt`  
includes the command you ran it with (some older example output files do not include this)


#### comparison

only affects the \# of requirements considered fulfilled and does not include [writing intensives](#writing-intensive-optional)

`>=` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **\[default]** &nbsp;&nbsp; e.g. 2 or more

`==` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.g. exactly 1


#### writing intensive

<sub>not included in the number of requirements</sub>

default shows all classes 

`y/Y` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; writing intensives only

`n/N` &nbsp;&nbsp;&nbsp;&nbsp; no writing intensives

&nbsp; 



### [requirements](data/) fulfilled 

add [requirements](data/) you've fulfilled to [taken.txt](user/taken.txt)

```
fcc_creative
plurdiv_d
```

*check **[degreeworks](https://degreeworks.cuny.edu/)** for everything, put them **exactly** as they correspond to the file names in **[requirements](data/) excluding the file extension*** 

&nbsp;  
`rc_whatever` &nbsp;&nbsp; required core  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `rc_eng_comp`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `rc_sci`  

&nbsp;  
`fcc_whatever` &nbsp;&nbsp; flexible common core  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `fcc_creative`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `fcc_ind`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `fcc_us`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `fcc_world`  

&nbsp;  
`plurdiv_x` &nbsp;&nbsp; pluralism and diversity  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `plurdiv_a`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `plurdiv_b`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `plurdiv_c`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `plurdiv_d`  

&nbsp; 


### scraping courses

gets the names + a link to the course description 

```
(venv) $ python scrape.py 
```

<sub>you will need `bs4` `(beautifulsoup4)` for this, [installation instructions below &or;](#installation)</sub>  

&nbsp; 



## installation 

`bs4` `(beautifulsoup4)` for scraping the course data 

```
(venv) $ pip install bs4
```

1. activate your virtual environment (make it if you don't have one)
   ```
   $ python3 -m venv venv
   $ . path/to/venv/bin/activate
   ```

2. or upgrade `pip` and install the dependencies using `requirements.txt`

   ```
   (venv) $ pip install --upgrade pip
   (venv) $ pip install -r requirements.txt
   ```
   while it is best to do this, you may very well just be able to `pip install bs4` and be done with it 

3. you're ready to go! 

&nbsp; 



## examples

#### basic

```
(venv) $ python classes.py -f 2 -l 4 -o out.txt
```


#### classes that fulfill 1 requirement
```
(venv) $ python classes.py -f 1 -l 4 -c "=="
```


#### writing intensive classes that fulfill 2 or more requirements 
```
(venv) $ python classes.py -f 2 -f 4 -c ">=" --wi y
```


#### non-writing intensive classes that fulfill 1 requirement
```
(venv) $ python classes.py -f 1 -l 4 -o out.txt -c "==" --wi n
```
