from pathlib import Path

import pytest
from click.testing import CliRunner

from .crawler import *

s3bucket = 'openneuro'
prefix = 'ds000003/ds000003_R2.0.2/uncompressed'
subject = "sub-01"

# s3bucket = 'fcp-indi'
# prefix = 'data/Projects/RocklandSample/RawDataBIDSLatest'
# subject = "sub-A00085864"

def test_subject_crawler():
    collect_files = subject_crawler(s3bucket, prefix, subject)
    for f in collect_files:
        assert type(f) == str
        assert subject in f

def test_parse_line():
    content = f'data/{subject}/func/{subject}_task-rest_bold.nii.gz'
    row = parse_line(s3bucket, subject, content)
    assert row[0] == f"s3://{s3bucket}/{content}"
    assert row[1] == f"s3://{s3bucket}/data"
    assert row[2] == subject
    assert row[3] == f"func/{subject}_task-rest_bold.nii.gz"

# test for cli
@pytest.fixture
def runner():
    return CliRunner()

def test_publiccrawler(runner, tmpdir):
    result = runner.invoke(cli,
        ["--s3bucket", s3bucket,
         "--prefix", prefix,
         "--output", tmpdir,
         subject])
    output = Path(tmpdir) / f"{subject}.tsv"
    assert result.exit_code == 0
    assert output.is_file()
    with open(output) as f:
        data = f.readlines()
    assert data[0].split() == headers
    assert subject in data[1].split()

    result = runner.invoke(cli, ["--help"])
    assert "Usage: s3crawler" in result.output
    assert result.exit_code == 0
