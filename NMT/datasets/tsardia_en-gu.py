import argparse
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
        help="If this flag isn't provided, new independent standard directory will be made for this dataset and it won't be joined within data/ folders in the data_path..",
    )

    parser.add_argument(
        "--delete_old",
        action="store_true",
        help="If this flag is provided, dataset from previous steps of pipeline will be deleted. Use this when you have less memory or huge dataset.",
    )

    args = parser.parse_args()

    # Download dataset
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/shahparth123/eng_guj_parallel_corpus/master/train.en",
        os.path.join(args.data_path, 'train.en')
    )
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/shahparth123/eng_guj_parallel_corpus/master/train.gu",
        os.path.join(args.data_path, 'train.gu')
    )

    # Transform the cleaned dataset to the standard format, in data_path/datai/
    en_path = os.path.join(args.data_path, "train.en")
    gu_path = os.path.join(args.data_path, "train.gu")
    final_data_path = next_datai(args.data_path)
    
    if args.delete_old:
        os.rename(en_path, os.path.join(final_data_path, 'para', 'en-gu.en'))
        os.rename(gu_path, os.path.join(final_data_path, 'para', 'en-gu.gu'))    
    else:
        shutil.copyfile(en_path, os.path.join(final_data_path, 'para', 'en-gu.en'))
        shutil.copyfile(gu_path, os.path.join(final_data_path, 'para', 'en-gu.gu'))    
    
    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
