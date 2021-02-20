from pathlib import Path

import pytest
from click.testing import CliRunner

from .crawler import *

s3bucket = 'openneuro'
prefix = 'ds000003/ds000003_R2.0.2/uncompressed'

def test_subject_crawler():
    sub = "sub-03"
    collect_files = subject_crawler(s3bucket, prefix, sub)
    for f in collect_files:
        assert type(f) == str

def test_parse_line():
    content = 'data/sub-01/func/sub-01_task-rest_bold.nii.gz'
    subject = "sub-01"
    row = parse_line(s3bucket, subject, content)
    assert row[0] == f"s3://{s3bucket}/{content}"
    assert row[1] == f"s3://{s3bucket}/data"
    assert row[2] == subject
    assert row[3] == "func/sub-01_task-rest_bold.nii.gz"

# test for cli
@pytest.fixture
def runner():
    return CliRunner()

def test_publiccrawler(runner, tmpdir):
    result = runner.invoke(cli,
        ["--s3bucket", s3bucket,
         "--prefix", prefix,
         "--output", tmpdir,
         "sub-01"])
    output = Path(tmpdir) / "sub-01.tsv"
    assert result.exit_code == 0
    assert output.is_file()
    with open(output) as f:
        data = f.readlines()
    assert data[0].split() == headers

    result = runner.invoke(cli, ["--help"])
    assert "Usage: s3crawler" in result.output
    assert result.exit_code == 0
