# pylint: disable=wrong-import-position
import os
import sys
import click

sys.path.insert(0, "/".join(os.path.dirname(__file__).split('/')[:-1]))

from spdxmerge.SPDXMergeLib import create_merged_spdx_document, write_file
from spdxmerge.utils import read_docs


@click.command()
@click.option("--docpath", prompt="Directory path", required=True,
              help="Directory path with SPDX files to be merged")
@click.option("--outpath", prompt="Output directory path", required=False, prompt_required=False,
              help="Output directory path where merged file should be saved")
@click.option("--name", prompt="Product Name", required=True,
              help="Name of product for which SBoM is created")
@click.option("--version", prompt="Product Version", required=True,
              help="Version of product for which SBoM is created")
@click.option("--mergetype", prompt="Shallow Merge -0 or Deep Merge-1",
              help="Enter 0 for shallow merge , 1 for deep merge", type=click.Choice(['0', '1']), default='1')
@click.option("--author", prompt="SBoM Author name", required=True,
              help="Author who is writing SBoM")
@click.option("--email", prompt="SBoM Author email", required=False, prompt_required=False,
              help="Author email address")
@click.option("--docnamespace", prompt="Document namespace",
              help="URL where document is stored or organization URL", default="https://spdx.organization.name")
@click.option("--filetype", prompt="SBoM output file type SPDX tag value format - T or JSON - J",
              help="Enter T for SPDX tag value format, J for JSON",
              type=click.Choice(['T', 't', 'J', 'j']), default='J')
def main(docpath, name, version, mergetype, author, email, docnamespace, filetype, outpath=None):
    """Tool provides option to merge SPDX SBoM files. Provides two options for merging,
    Shallow Merge: New SBoM is created only with external ref links to SBoM files to be merged
    Deep Merge: New SBoM file is created by appending package, relationship, license information
    """
    doc_list = read_docs(docpath)
    merge_type = "shallow" if mergetype == '0' else "deep"
    doc = create_merged_spdx_document(doc_list, docnamespace, name, version, author, email, merge_type)
    write_file(doc, filetype, merge_type, outpath)


if __name__ == "__main__":
    main()
