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

Create a subdataset for one subjuct with `datalad addurls`

```bash
S3BUCKET='fcp-indi'
PREFIX='data/Projects/RocklandSample/RawDataBIDSLatest'
sub="sub-A00085864"

if [[ ! -f  ~/.config/datalad/procedures/cfg_public_s3.sh ]]; then
   echo "Add configuration for datalad remote"
   mkdir -p ~/.config/datalad/procedures/
   echo "git annex initremote datalad type=external externaltype=datalad encryption=none" \
      > ~/.config/datalad/procedures/cfg_public_s3.sh
fi

datalad create -d testds -c public_s3
cd testds
s3crawler ${sub} --s3bucket $S3BUCKET --prefix $PREFIX --output .git/
datalad addurls -d testds/${sub} -c public_s3 \
   --ifexists skip .git/${sub}.tsv '{original_path}' '{filename}'
datalad drop -d testds/${sub} -r --nocheck  # remove data to save disc space
```
