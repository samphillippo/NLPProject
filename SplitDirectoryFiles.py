import os

FOLDER_PATH = './test_json'
NUM_SPLITS = 5


if __name__ == '__main__':
    
    filepaths = list(sorted(map((lambda file: FOLDER_PATH + '/' + file), filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH))), key=(os.path.getsize)))

    split_idx = 0

    for file in filepaths:

        dirname = os.path.join(FOLDER_PATH, 'split_' + str(split_idx))

        os.makedirs(dirname, exist_ok=True)

        destination = os.path.join(dirname, os.path.basename(file))

        os.replace(file, destination)

        split_idx = (split_idx + 1) % NUM_SPLITS