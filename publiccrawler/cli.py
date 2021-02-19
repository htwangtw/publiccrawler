from pathlib import Path
import click
from .crawler import subject_crawler, save_addurls_table

@click.command()
@click.option('--s3bucket',
    help='s3 bucket name', type=str)
@click.option('--prefix',
    help='path to your target dataset folder', type=str)
@click.option('--output',
    help='save file where', type=click.Path(exists=True))
@click.argument('subject', type=str)

def main(s3bucket: str, prefix:str , subject:str, output: str):
    """
    stuff
    """
    collect_files = subject_crawler(s3bucket, prefix, subject)
    save_addurls_table(collect_files, s3bucket, Path(output) / f"{subject}.tsv")

if __name__ == "__main__":
    main()