# Tool for merging SPDX files

This tool integrates multiple SPDX JSON formatted Software Bill of materials (SBOMs) into a parent SBOM, either by consolidating all the contents into a single file or by creating references to multiple files.
The tool works with SPDX 2.2 and SPDX 2.3 version.

## Features

Combine multiple SPDX JSON/Tag value files into a single parent Software Bill of Materials (SBOM) in one of two ways.

- Deep Merge - Combines the contents of all SBOM files into a single comprehensive parent file, incorporating all the information about the package dependencies and their relationships.
- Shallow Merge - Generates a parent SBOM that references multiple SBOM files in the 'externalDocumentRefs' section.

## How to use

### Manual Installation

SPDX Tools(spdx-tools) needs to be installed as a pre-requisite for this application to work. It is listed in the requirement.txt file.
Just run the below command to install all the requirements that needs to be installed.

```shell
pip install -r requirements.txt
```

Execute the command with the required inputs.
  
```shell
    python src/SPDXMerge --docpath <folder path of the SBOMs to be merged>
                         --name <product name>
                         --mergetype <0 for deep merge/1 for shallow merge>
                         --author <organization or author name>
                         --email <org/ author email>
                         --docnamespace <namespace for spdx doc>
                         --filetype <expected SBOM file format for JSON/T for Tag value>
```

### GitHub action

```yml
  - name: Checkout project
    uses: actions/checkout@v3
  - name: Run SPDX Merge tool to merge spdx files 
    uses: philips-software/SPDXMerge@v0.1
    with:
      docpath: ${{github.workspace}}/Test # path with spdx files in json
      name: sample-sbom                   # name project
      mergetype: 1                        # 0 shallow merge, 1 deep merge defaults 1
      author: "Kung Fury"                 # Author
      email: "kfury@example.com"          # email - optional
      filetype: J                         # expected SBOM format JSON/ tag value format , defaults to J
      docnamespace: "https://mycompany.example.com"
  - name: Check result
    run: cat merged-SBoM.json
```

### Docker image

```shell
docker run -it --rm -v$(PWD):/code \
  -e DOCPATH='/code' \
  -e NAME='' \
  -e MERGETYPE='' \
  -e AUTHOR='' \
  -e EMAIL='' \
  -e DOCNAMESPACE='' \
  -e FILETYPE='' \
  docker.io/philipssoftware/spdxmerge:v0.1.0
```

## TODOs

- Option for Organization, Author tag in document creation
