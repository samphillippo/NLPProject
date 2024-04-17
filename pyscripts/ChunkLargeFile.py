import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def utf8len(s):
    return len(s.encode('utf-8'))


def chunk_json_file_write_while_going(filepath, out_dir_prefix, json_MB_chunk=100, compress=True):
    current_KB_size = 0
    num_chunks_made = 0

    chunked_filepaths = []

    with open(filepath, 'r') as f:

        out_path = '{}_{:03d}.json'.format(out_dir_prefix, num_chunks_made)
        chunked_filepaths.append(out_path)
        out_chunk_file = open(out_path, 'w')

        for line in f:
            bytes_size = utf8len(line)
            current_KB_size += (bytes_size / 1000.0)

            out_chunk_file.write(line + '\n')

            if current_KB_size >= json_MB_chunk * 1000:

                out_chunk_file.close()
                if compress:
                    os.system('xz {}'.format(out_path))

                current_KB_size = 0
                num_chunks_made += 1

                out_path = '{}_{:03d}.json'.format(out_dir_prefix, num_chunks_made)
                chunked_filepaths.append(out_path)
                out_chunk_file = open(out_path, 'w')

        out_chunk_file.close()
        if compress:
            os.system('xz {}'.format(out_path))

    return chunked_filepaths


def chunk_xz_file(filepath):
    os.system('unxz {}'.format(filepath))
    file_prefix = filepath.split('.json')[0]
    json_path = file_prefix + '.json'
    chunked_filepaths = chunk_json_file_write_while_going(json_path, file_prefix)
    os.remove(json_path)
    return chunked_filepaths




def find_xz_files_above_size(folderpath, xz_MB_min_size=150):
    filenames = list(filter(lambda x: x.endswith('.xz') and ((os.path.getsize(folderpath + '/' + x) / 1000.0) > (xz_MB_min_size * 1000.0)), os.listdir(folderpath)))
    return filenames



def chunk_all_files_in_folder(directory):
    files = find_xz_files_above_size(directory, xz_MB_min_size=100)
    print("Chunking {} files".format(len(files)))
    for index, file in enumerate(files):
        chunk_xz_file(directory + '/' + file)
        print("Chunked {}".format(file))
    return directory



FOLDERS = ['/scratch/selvitelli.n/dataset/split_0', '/scratch/selvitelli.n/dataset/split_1']


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(chunk_all_files_in_folder, folder) for folder in FOLDERS]
        for future in as_completed(futures):
            result = future.result()
            print("Completed chunking {}".format(result))


# if __name__ == '__main__':
#     files = find_xz_files_above_size(FOLDER, xz_MB_min_size=100)

#     print("Found {} files to chunk".format(len(files)))

#     total_time = time()

#     for index, file in enumerate(files):
#         print("Chunking {} ({}/{})\n - Extracting file to json...".format(file, index + 1, len(files)))
#         local_time = time()

#         chunked_files = chunk_xz_file(FOLDER + '/' + file)
#         num_chunks = len(chunked_files)

#         print(" - Split {} into {} chunks ({} secs)\n".format(file, num_chunks, round((time() - local_time), 2)))

#     print("Complete. ({} secs)".format(round((time() - total_time), 2)))
