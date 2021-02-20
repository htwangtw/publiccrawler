[![test and coverage](https://github.com/htwangtw/publiccrawler/actions/workflows/test_coverage.yml/badge.svg)](https://github.com/htwangtw/publiccrawler/actions/workflows/test_coverage.yml)
[![codecov](https://codecov.io/gh/htwangtw/publiccrawler/branch/main/graph/badge.svg?token=PHRJJHCaHA)](https://codecov.io/gh/htwangtw/publiccrawler)


# Public Crawler

Generate `datalad addurls` required URL-FILE input from public AWS S3 bucket.
This project is inspired by Datalad Handbook chapter: [Scaling up: Managing 80TB and 15 million files from the HCP release](http://handbook.datalad.org/en/latest/usecases/HCP_dataset.html).
Current implementation is only for AWS public access buckets?

## Installation
```
pip install git+https://github.com/htwangtw/publiccrawler.git
```

## Usage
Modified from [Datalad Handbook example on HPC](http://handbook.datalad.org/en/latest/usecases/HCP_dataset.html#dataset-creation-with-datalad-addurls)
```bash
S3BUCKET='fcp-indi'
PREFIX='data/Projects/RocklandSample/RawDataBIDSLatest'
sub="sub-A00085864"
datalad create -d test -c public_s3
s3crawler ${sub} --s3bucket $S3BUCKET --prefix $PREFIX --output .git/
datalad addurls -d test/${sub} -c public_s3 \
   --ifexists skip .git/${sub}.tsv '{original_path}' '{filename}'
datalad drop -d test/${sub} -r --nocheck ${sub}.tsv  # remove data to save space
```
