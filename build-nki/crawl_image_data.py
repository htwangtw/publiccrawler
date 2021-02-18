from pathlib import Path
import sys
import csv

import boto3

from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing


if __name__ == "__main__":
    sub = sys.argv[1]
    s3_bucket_name = 'fcp-indi'
    bids_prefix = 'data/Projects/RocklandSample/RawDataBIDSLatest/'

    # set up s3 bucket
    s3 = boto3.resource('s3')
    s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    s3_bucket = s3.Bucket(s3_bucket_name)
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    # get all file paths on s3
    def subject_crawler(sub):
        bidsfiles = s3_client.list_objects_v2(Bucket=s3_bucket_name,
            Prefix=bids_prefix + f"sub-{sub}/")
        return [d["Key"]for d in bidsfiles["Contents"]]

    collect_files =subject_crawler(sub)

    # create datalad addurls table
    headers = ["original_path", "bidsroot", "subject", "filename", "ext"]

    # save table
    with open(f"subject_tables/sub-{sub}_table.tsv", mode="w") as f:
        table_writer = csv.writer(f, delimiter="\t")
        table_writer.writerow(headers)
        for opath in collect_files:
            original = f"s3://{s3_bucket_name}/{opath}"
            bidsroot, filename = original.split(f"sub-{sub}/")
            ext = (".").join(filename.split(".")[1:])
            filename = filename.split(".")[0]
            table_writer.writerow([original, bidsroot, f"sub-{sub}", filename, ext])
