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
print(fileExists(add2))

```
```py
True
<InvalidFile>
```

___
#### dirExists

_Raise_: \<InvalidDir\>

```py
from fileUts import dirExists

add1 = "c:/mydir/myfile.ext"
add2 = "c:/mydir"

print(dirExists(add1))
print(dirExists(add2))

```
```py
<InvalidDir>
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
print(getFileExtenssion(add2))

```
```py
'ext'
<InvalidFile>
```


