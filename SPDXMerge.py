import utils
from  SPDXMergeLib import SPDXDeepMerge_list,SPDXShallowMerge_list


import click

@click.command()
@click.option("--docpath", prompt="Directory path",help="Directory path with SPDX files to be merged")
@click.option("--name",prompt="Product Name",help="Name of product for which SBoM is created")
@click.option("--type",prompt="Shallow Merge -0 or Deep Merge-1", help="Enter 0 for shallow merge , 1 for deep merge", default=1)
@click.option("--author",prompt="SBoM Author name", help="Author who is writing SBoM")              # TODO will the user have optoin to give organization or person as author ? 
@click.option("--docnamespace",prompt="Document namespace", help="URL where document is stored or organzation URL", default="https://spdx.organization.name")  # TODO this needs to be check in SPDX document for help text  ? 

def main(docpath,name, type, author, docnamespace):
    """    Tool provides option to merge SPDX SBoM files. Provies two options for merging, 
           Shallow Merge : New SBoM is created only with external ref links to SBoM files to be merged 
           Deep Merge : New SBoM file is created by appending package , relationship , license information
    """
    doc_list = utils.read_docs(docpath)
    
    if type == 1: 
        doc =SPDXDeepMerge_list(doc_list,docnamespace,name,author)
    elif type ==0:
        doc =SPDXShallowMerge_list(doc_list,docnamespace,name,author)
    

    #spdx_deep_merge(dir,name="AirTrack",author="Philips",docnamespace="https://spdx.philips.com")

if __name__ == "__main__":
    main()


