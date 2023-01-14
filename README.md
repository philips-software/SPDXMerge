# Tool for merging SPDX files 
This tool provides option to merge multiple SPDX file by taking SPDX files folder path as input. 

# Features
* Merge multiple SPDX files 
* Can merge by copying all package in single file (Deep Merge Option)
* Can merge by creating external referances (Shallow Merge Option)

# Installation
This tool needs SPDX Tools library to be installed, It is recommened to create virtual environment to install this tool. 
Follow below steps 
1. Create virtual environment 
```
  python -m venv ./venv
```
2. Go to virtual environment path  ( in case of Windows venv\Scripts)
```
  cd venv\bin
```
3. Install it from PyPI with in virtual environment created 
```
  pip install spdx-tools 
```


# How to use 
* For Deep Merge 
```
    SPDXMerge --docpath <SPDX input folder path> --type 0 --author <Mention Organization or Author> --docnamespace <namespace for spdx doc> --name <product name>
```

* For Shallow Merge 
```
    SPDXMerge --docpath <SPDX input folder path> --type 1 --author <Mention Organization or Author> --docnamespace <namespace for spdx doc> --name <product name>'
```

# TODOs
* In case of deep merge -  removal of duplicates 
* Option for Organization, Author tag in documentcreation
