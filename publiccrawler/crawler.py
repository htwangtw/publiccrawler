from pathlib import Path
import re
import csv

import boto3
from botocore import UNSIGNED
from botocore.client import Config

import click

# create datalad addurls table
headers = ["original_path", "parent_path", "subject", "filename"]

def subject_crawler(s3bucket, prefix, subject):
    s3_client = boto3.client('s3',
                             config=Config(signature_version=UNSIGNED))
    bidsfiles = s3_client.list_objects_v2(
        Bucket=s3bucket,
        Prefix=f"{prefix}/{subject}/")
    return [d["Key"] for d in bidsfiles["Contents"]]

def parse_line(s3bucket, subject, content):
    original = f"s3://{s3bucket}/{content}"
    parent, filename = original.split(f"/{subject}/")
    return [original, parent, f"{subject}", filename]

def save_addurls_table(collect_files, output):
    # save table
    with open(output, mode="w") as f:
        table_writer = csv.writer(f, delimiter="\t")
        table_writer.writerow(headers)
        for l in collect_files:
            table_writer.writerow(l)

# command line tool
@click.command(name="s3crawler")
@click.option('--s3bucket',
    help='s3 bucket name', type=str)
@click.option('--prefix',
    help='path to your target dataset folder', type=str)
@click.option('--output',
    help='save file where', type=click.Path(exists=True))
@click.argument('subject', type=str)

def cli(s3bucket: str, prefix:str , subject:str, output: str):
    """
    Command line tool to create datalad addurls input from AWS s3 bucket.
    The output split full file path by subject ID / or any other subsirectory name (SUBJECT)
    The rest of the path to the files will be preserved.

    Example:
    > s3crawler sub-01 --s3bucket openneuro --prefix ds000003/ds000003_R2.0.2/uncompressed/data
    This command will get all paths to files under this path:
    s3://openneuro/ds000003/ds000003_R2.0.2/uncompressed/data/sub-01/
    A path would be broken down in the following manner:
    s3://openneuro/ds000003/ds000003_R2.0.2/uncompressed/data/sub-01/func/sub-01_task-rest_bold.nii.gz
    original_path: same as above
    parent_path: s3://openneuro/ds000003/ds000003_R2.0.2/uncompressed/data
    subject: sub-01
    filename: func/sub-01_task-rest_bold.nii.gz

    The output file in this example (sub-01.tsv) can be passed to datalad addurls
    to create a dataset and preserve all structure detailed as filename in your datalad dataset.
    datalad addurls -d testds/sub-01 \
            ./sub-01.tsv '{original_path}' '{filename}'
    """
    file_paths = subject_crawler(s3bucket, prefix, subject)
    parsed_files = [parse_line(s3bucket, subject, content) for content in file_paths]
    save_addurls_table(parsed_files, Path(output) / f"{subject}.tsv")

if __name__ == "__main__":
    cli()