import pickle
import random
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--list_indices_path', type=str)
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--seed', type=int, default=1)
    args = parser.parse_args()

    nb_training_entries = 18500
    nb_validation_entries = 1000
    
    with open(args.list_indices_path, 'rb') as handle:
            list_indices = pickle.load(handle)

    seed = args.seed
    random.seed(seed)

    # select training indices
    training_indices = random.sample(list_indices, nb_training_entries)

    # select non training indices
    non_training_indices = [indice for indice in list_indices if indice not in training_indices]

    # select validation indices
    validation_indices = random.sample(non_training_indices, nb_validation_entries)

    training_indices_str = set(str(ind) for ind in training_indices)
    validation_indices_str = set(str(ind) for ind in validation_indices)

    output_dir = args.output_dir

    print("Saving {p}/training_indices_seed{s}.pickle ({n} indices)".format(p = output_dir, s = seed, n = len(training_indices_str)))
    with open(output_dir + '/training_indices_seed{s}.pickle'.format(s = seed), 'wb') as handle_1:
        pickle.dump(training_indices_str, handle_1, protocol=pickle.HIGHEST_PROTOCOL)

    print("Saving {p}/validation_indices_seed{s}.pickle ({n} indices)".format(p = output_dir, s = seed, n = len(validation_indices_str)))    
    with open(output_dir + '/validation_indices_seed{s}.pickle'.format(s = seed), 'wb') as handle_2:
        pickle.dump(validation_indices_str, handle_2, protocol=pickle.HIGHEST_PROTOCOL)
