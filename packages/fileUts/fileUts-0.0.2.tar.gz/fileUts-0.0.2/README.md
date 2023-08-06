# fileUts
#
### Installation

```sh
pip install fileUts
```

### Usages
#
___
#### isDir
```py
from fileUts import isDir

add1 = "c:/mydir"
add2 = "c:/mydir/myfile.ext"

print(isDir(add1))
print(isDir(add2))

```
```py
True
False
```
___
#### isFile
```py
from fileUts import isFile

add1 = "c:/mydir"
add2 = "c:/mydir/myfile.ext"

print(isFile(add1))
print(isFile(add2))

```
```py
False
True
```
___
#### fileExists

_Raise_: \<InvalidFile\>

```py
from fileUts import fileExists

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir"

print(fileExists(add1))
print(fileExists(add2)) # raises a <InvalidFile>

```
```py
True
```

___
#### dirExists

_Raise_: \<InvalidDir\>

```py
from fileUts import dirExists

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir"

print(dirExists(add1)) # raises a <InvalidDir>
print(dirExists(add2))

```
```py
True
```

___
#### getFileExtenssion

_Raise_: \<InvalidFile\>

```py
from fileUts import getFileExtenssion

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir"

print(getFileExtenssion(add1))
print(getFileExtenssion(add2)) # raises a <InvalidFile>

```
```py
'ext'
```


___
#### createDir

_Raise_: \<InvalidDir\>

```py
from fileUts import createDir

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir"

print(createDir(add1)) # raises a <InvalidDir>
print(createDir(add2))

```
```py
True
```

___
#### createDir

_Raise_: \<InvalidDir\>

```py
from fileUts import createDir

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir/mydir2/mydir3"

print(createDir(add1)) # raises a <InvalidDir>
print(createDir(add2))

```
```py
True
```

___
#### moveFiles

_Raise_: \<InvalidDir\>

```py
from fileUts import moveFiles

files   = "c:/mydir/myfile.*"
to_addr = "c:/target_dir"

print(moveFiles(files,to_addr))

```
```py
1
```

___
#### clearDir

_Raise_: \<InvalidDir\>

```py
from fileUts import clearDir

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir" 

clearDir(add1) # raises a <InvalidDir>
clearDir(add2)

```
___
#### renameFile

_Raise_: \<InvalidDir\>

```py
from fileUts import renameFile

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir" 

renameFile(add1,'newname.ext')
renameFile(add2,,'newname.ext') # raises a <InvalidFile>

```



