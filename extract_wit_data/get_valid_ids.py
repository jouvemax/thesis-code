import argparse
import pickle
import h5py

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_features', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--file_name', type=str, default="valid_ids")
    args = parser.parse_args()

    f = h5py.File(args.path_to_features, 'r')
    valid_entries = f.keys()
    valid_ids = list(valid_entries)

    print("{n} successfully extracted features.".format(n = len(valid_ids)))
    print("Saving valid ids at {p}/{f}.pickle.".format(p = args.output_path, f = args.file_name))

    with open(args.output_path + "/" + args.file_name + ".pickle", 'wb') as handle:
        pickle.dump(valid_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)