import sys
import re
import csv

import boto3

from botocore import UNSIGNED
from botocore.client import Config

# create datalad addurls table
headers = ["original_path", "bidsroot", "subject", "filename"]

def subject_crawler(s3_bucket_name, bids_prefix, sub):
    s3_client = boto3.client('s3',
                             config=Config(signature_version=UNSIGNED))
    bidsfiles = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Prefix=bids_prefix + f"/{sub}/")
    return [d["Key"] for d in bidsfiles["Contents"]]

def parse_line(s3_bucket_name, content):
    original = f"s3://{s3_bucket_name}/{content}"
    sub = re.search(r'\/(sub-[a-zA-Z0-9]*)\/', content).group(1)
    bidsroot, filename = original.split(f"/{sub}/")
    return [original, bidsroot, f"{sub}", filename]

def save_addurls_table(collect_files, s3_bucket_name, output):
    # save table
    with open(output, mode="w") as f:
        table_writer = csv.writer(f, delimiter="\t")
        table_writer.writerow(headers)
        for content in collect_files:
            cur_row = parse_line(s3_bucket_name, content)
            table_writer.writerow(cur_row)