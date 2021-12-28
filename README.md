# defendit

## package on linux
```
pyinstaller --clean   --add-data "resources/*:." --hidden-import='PIL._tkinter_finder'  -F  defendit.py
cp resources/* dist
```

## package pc
```
pyinstaller --clean   --add-data "resources\*;." --hidden-import='PIL._tkinter_finder'  -F  defendit.py
copy resources\* dist
```

