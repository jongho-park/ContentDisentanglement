import os
import os.path as osp
import argparse
import json
import re


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('trainset_fpath', help='Path to the train imageset file.')
    parser.add_argument('annotation_fpath', help='Path to the annotation file.')
    parser.add_argument('dst_dir', help='Directory of the destination folder to create.')

    args = parser.parse_args()

    return args


_RE_DOUBLE_DIVIDED = r'^train(?P<t_fold>[0-9]+)_(?P<v_fold>[0-9]+).txt$'
_RE_SINGLE_DIVIDED = r'^train(?P<v_fold>[0-9]+).txt$'
_RE_NOT_DIVIDED = r'^train.txt$'


def _get_train_test_fnames(trainset_fpath):
    fname = osp.basename(trainset_fpath)
    if re.match(_RE_DOUBLE_DIVIDED, fname) is not None:
        gdict = re.match(_RE_DOUBLE_DIVIDED, fname).groupdict()
    elif re.match(_RE_SINGLE_DIVIDED, fname) is not None:
        gdict = re.match(_RE_SINGLE_DIVIDED, fname).groupdict()
    elif re.match(_RE_NOT_DIVIDED, fname) is not None:
        gdict = re.match(_RE_NOT_DIVIDED, fname).groupdict()

    validset_fname, testset_fname = 'validation', 'test'
    if 't_fold' in gdict:
        validset_fname += '{}_'.format(gdict['t_fold'])
        testset_fname += '{}'.format(gdict['t_fold'])
    if 'v_fold' in gdict:
        validset_fname += '{}'.format(gdict['v_fold'])
    validset_fname += '.txt'
    testset_fname += '.txt'
    validset_fpath = osp.join(osp.dirname(trainset_fpath), validset_fname)
    testset_fpath = osp.join(osp.dirname(trainset_fpath), testset_fname)

    with open(trainset_fpath, 'r') as f:
        train_list = [x.strip() for x in f.readlines()]
    with open(validset_fpath, 'r') as f:
        valid_list = [x.strip() for x in f.readlines()]
    train_list = train_list + valid_list

    with open(testset_fpath, 'r') as f:
        test_list = [x.strip() for x in f.readlines()]

    return train_list, test_list


def _write_sample_lists(trainset_fpath, annotation_fpath, dst_dir):
    with open(annotation_fpath, 'r') as f:
        anno = json.load(f)

    train_fnames, test_fnames = _get_train_test_fnames(trainset_fpath)
    trainA, trainB, testA, testB = [], [], [], []
    for fname in train_fnames:
        if anno['images'][fname]['class'][0] == 0:
            trainB.append(fname)
        else:
            trainA.append(fname)
    for fname in test_fnames:
        if anno['images'][fname]['class'][0] == 0:
            testB.append(fname)
        else:
            testA.append(fname)

    root_dir = osp.realpath(trainset_fpath[:trainset_fpath.index('imageset')])
    img_dir = osp.join(root_dir, 'image')

    with open(osp.join(dst_dir, 'testA.txt'), 'w') as f:
        f.writelines([osp.join(img_dir, x + '\n') for x in testA])
    with open(osp.join(dst_dir, 'testB.txt'), 'w') as f:
        f.writelines([osp.join(img_dir, x + '\n') for x in testB])
    with open(osp.join(dst_dir, 'trainA.txt'), 'w') as f:
        f.writelines([osp.join(img_dir, x + '\n') for x in trainA])
    with open(osp.join(dst_dir, 'trainB.txt'), 'w') as f:
        f.writelines([osp.join(img_dir, x + '\n') for x in trainB])


if __name__ == '__main__':
    args = _parse_args()

    if not osp.exists(args.dst_dir):
        os.makedirs(args.dst_dir)

    _write_sample_lists(args.trainset_fpath, args.annotation_fpath, args.dst_dir)
