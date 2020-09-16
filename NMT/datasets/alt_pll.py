import argparse
from ...utils import extract_file
from ..utils import joiner, next_datai
import urllib.request
import os, shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        required=True,
        help="Path to directory where you want to store data, or path to existing data. data/ will be created or should exist inside this.",
    )

    parser.add_argument(
        "--merge",
        action="store_true",
        help="If this flag isn't provided, new independent standard directory will be made for this dataset and it won't be joined within data/ folders in the data_path.",
    )

    parser.add_argument(
        "--delete_old",
        action="store_true",
        help="If this flag is provided, dataset from previous steps of pipeline will be deleted. Use this when you have less memory or huge dataset.",
    )

    args = parser.parse_args()

    # Download dataset
    urllib.request.urlretrieve(
        "http://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206.zip",
        os.path.join(args.data_path, 'ALT-Parallel-Corpus-20191206.zip')
    )

    # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.
    alt_path = "ALT-Parallel-Corpus-20191206.zip"
    extract_file(os.path.join(args.data_path, alt_path))

    # Transform the cleaned dataset to the standard format, in data_path/datai/
    en_path = os.path.join(args.data_path, alt_path, "data_en.txt")
    bn_path = os.path.join(args.data_path, alt_path, "data_bg.txt")
    hi_path = os.path.join(args.data_path, alt_path, "data_hi.txt")
    final_data_path = next_datai(args.data_path)
    
    shutil.copyfile(en_path, os.path.join(final_data_path, 'para', 'bn-en.en'))
    if args.delete_old:
        os.rename(en_path, os.path.join(final_data_path, 'para', 'en-hi.en'))
        os.rename(hi_path, os.path.join(final_data_path, 'para', 'en-hi.hi'))
        os.rename(bn_path, os.path.join(final_data_path, 'para', 'bn-en.bn'))    
    else:
        shutil.copyfile(en_path, os.path.join(final_data_path, 'para', 'en-hi.en'))
        shutil.copyfile(hi_path, os.path.join(final_data_path, 'para', 'en-hi.hi'))
        shutil.copyfile(bn_path, os.path.join(final_data_path, 'para', 'bn-en.bn'))    
    
    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
