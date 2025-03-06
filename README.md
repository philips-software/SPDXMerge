# Tool for merging SPDX files  

This tool integrates multiple SPDX JSON formatted Software Bill of Materials (SBOMs) into a parent SBOM, either by consolidating all the contents into a single file or by creating references to multiple files.  

The tool works with SPDX 2.2 and SPDX 2.3 versions.  

## Features  

Combine multiple SPDX JSON/Tag value files into a single parent Software Bill of Materials (SBOM) in one of two ways:  

- **Deep Merge** - Combines the contents of all SBOM files into a single comprehensive parent file, incorporating all the information about the package dependencies and their relationships.  
- **Shallow Merge** - Generates a parent SBOM that references multiple SBOM files in the `externalDocumentRefs` section.  

## How to use  

### Manual Installation  

SPDX Tools (`spdx-tools`) needs to be installed as a prerequisite for this application to work. It is listed in the `requirements.txt` file.  
Run the following command to install all necessary dependencies:  

```shell
pip install -r requirements.txt
```  

Execute the command with the required inputs:  

```shell
    python spdxmerge/SPDXMerge --docpath <folder path of the SBOMs to be merged>
                         --outpath <folder path where the merged file will be saved> (optional)
                         --name <product name>
                         --version <product version>
                         --mergetype <0 for deep merge/1 for shallow merge>
                         --author <organization or author name>
                         --email <org/author email>
                         --docnamespace <namespace for SPDX document>
                         --filetype <expected SBOM file format for JSON/T for Tag value>
                         --rootdocpath <expects SBOM file in the docpath that should act as the root doc> (optional)
```  
---

### 🔹 **New Update: Version Input**  
To establish a unique **"DESCRIBES"** relationship in the SPDX document, a **root package** must be created.  
For this, we now require both **name** and **version** as input parameters.  

---

### 🔹 **New Update: Roothpath input**  
To establish a unique **"DESCRIBES"** relationship in the SPDX document, a **root document** can be specified.  
For this, we now introduce the **`--rootdocpath`** option to define the root document, ensuring proper validation and relationship mapping.

#### Options
- `--rootdocpath` (optional): Specifies the root SBoM document.

#### Implementation Details
- The tool scans the root document for a `DESCRIBES` relationship.
- If found, the related SPDX element ID is used to establish the relationship.
- If no such relationship is found, an error is raised.
- The relationship is added to the master document.

#### Error Handling
- Raises an error if `--rootdocpath` is defined but the file is not found in the path.
- Raises an error if the root document lacks a `DESCRIBES` relationship.
---

### GitHub Action  

```yml
  - name: Checkout project
    uses: actions/checkout@v3
  - name: Run SPDX Merge tool to merge spdx files 
    uses: philips-software/SPDXMerge@v0.2.0
    with:
      docpath: ${{github.workspace}}/Test 
      name: sample-sbom                   
      version: 1.0.0                      
      mergetype: 1                         
      author: "Kung Fury"                  
      email: "kfury@example.com"          
      filetype: J                          
      docnamespace: "https://mycompany.example.com"
  - name: Check result
    run: cat merged-SBoM.json
```  

---

### Docker Image  

```shell
docker run -it --rm \
  -v $(PWD):/code \
  -v $(PWD)/output/:/output \
  -e DOCPATH='/code' \
  -e OUTPATH='/output' \
  -e NAME='' \
  -e VERSION='' \  
  -e MERGETYPE='' \
  -e AUTHOR='' \
  -e EMAIL='' \
  -e DOCNAMESPACE='' \
  -e FILETYPE='' \
  -e ROOTPATH='' \
  docker.io/philipssoftware/spdxmerge:v0.2.0
```  

---

## TODOs  

- Option for Organization, Author tag in document creation  

---
