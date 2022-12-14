# coding=utf-8
import sys
sys.path.append("../..")

from detectron2_proposal_maxnms_pretraining import collate_fn, extract, NUM_OBJECTS, DIM
from torch.utils.data import Dataset, DataLoader
import cv2
from tqdm import tqdm
from pathlib import Path
import argparse
import numpy as np


from multiprocessing import Pool


class ImageDataset(Dataset):
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.image_path_list = list(tqdm(image_dir.iterdir()))
        self.n_images = len(self.image_path_list)

    def __len__(self):
        return self.n_images

    def __getitem__(self, idx):

        image_path = self.image_path_list[idx]
        image_id = image_path.stem

        img = cv2.imread(str(image_path))

        return {
            'img_id': image_id,
            'img': img
        }


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--batchsize', default=1, type=int, help='batch_size')
    parser.add_argument('--root', type=str, default='datasets/flickr30k/')
    parser.add_argument('--outdir', type=str)
    parser.add_argument("--caption_path", type=str)
    args = parser.parse_args()

    dset_img_dir = Path(args.root).resolve()

    dataset_name = 'WIT'

    out_dir = Path(args.outdir).resolve()
    if not out_dir.exists():
        out_dir.mkdir()

    print('Load images from', dset_img_dir)
    print('# Images:', len(list(dset_img_dir.iterdir())))

    dataset = ImageDataset(dset_img_dir)

    # buggy image
    # print(dataset[9883])
    # {'img_id': '17363766', 'img': None}



    # for i, k in enumerate(dataset):
    #     if i % 200 == 0:
    #         print("Image # {index}".format(index = i))
    #     if k is None:
    #         continue
    #     if k['img'] is None:
    #         print(k['img_id'])

    dataloader = DataLoader(dataset, batch_size=args.batchsize,
                            shuffle=False, collate_fn=collate_fn, num_workers=4)


    # dataloader = DataLoader(dataset, batch_size=args.batchsize,
    #                         shuffle=False, num_workers=4)

    output_fname = out_dir.joinpath(f'{dataset_name}_boxes{NUM_OBJECTS}.h5')
    print('features will be saved at', output_fname)

    desc = f'{dataset_name}_{(NUM_OBJECTS, DIM)}'

    extract(output_fname, dataloader, desc, args.caption_path)