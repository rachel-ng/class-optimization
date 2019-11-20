# degree-planner

oh man i really spent like 4 hours writing this huh 

## terminal usage

```
$ python classes.py [reqs fulfilled] [hardness] [output] [fulfilled reqs] [comp] [writing intensive]
```

#### fulfilled requirements file (optional)

file name or &nbsp;&nbsp; `-` &nbsp;&nbsp; for none

#### comparison (optional)

`>=` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **\[default]** &nbsp;&nbsp; i.e. 2 or more

`==` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i.e. exactly 1

`-` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for use with [writing intensive option](#writing-intensive), uses the  &nbsp; **\[default]** &nbsp;&nbsp; `>=`


#### writing intensive (optional)

`WI` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; writing intensives only

`-WI` &nbsp;&nbsp;&nbsp;&nbsp; no writing intensives


### examples

#### basic

```
$ python classes.py 2 4 out.txt - 
```

#### classes that fulfill 1 requirement
```
$ python classes.py 1 4 out.txt - == 
```

#### writing intensive classes that fulfill 2 or more requirements 
```
$ python classes.py 2 4 out.txt - - WI           // lazy way
$ python classes.py 2 4 out.txt - >= WI
```

#### non-writing intensive classes that fulfill 1 requirement
```
$ python classes.py 1 4 out.txt - == -WI
```

#### non-writing intensive classes that fulfill 2 requirements not in taken.txt
```
$ python classes.py 2 4 out.txt taken.txt == -WI
```
taken.txt
```
fcc_creative
plurdiv_d
```
