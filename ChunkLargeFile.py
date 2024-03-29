import os
import math
from time import time


def utf8len(s):
    return len(s.encode('utf-8'))



def chunk_json_file_write_while_going(filepath, out_dir, prefix, json_MB_chunk=100, compress=True):
    current_KB_size = 0
    num_chunks_made = 0

    total_size_KB = os.path.getsize(filepath) / 1000.0
    total_chunks_expected = math.ceil(total_size_KB / (json_MB_chunk * 1000.0))

    print(" - {} expected to chunk into  {} (+/- 1) files".format(filepath, total_chunks_expected))
    local_time = time()

    with open(filepath, 'r') as f:

        out_path = '{}/{}_{:03d}.json'.format(filepath, prefix, num_chunks_made)
        out_chunk_file = open(out_path, 'w')

        for line in f:
            bytes_size = utf8len(line)
            current_KB_size += (bytes_size / 1000.0)

            out_chunk_file.write(line + '\n')

            if current_KB_size >= json_MB_chunk * 1000:

                out_chunk_file.close()
                if compress:
                    print(" - Compressing chunk {}...".format(out_path))
                    os.system('xz {}'.format(out_path))

                out_path = '{}/{}_{:03d}.json'.format(filepath, prefix, num_chunks_made)
                out_chunk_file = open(out_path, 'w')

                secs_passed = round((time() - local_time), 2)
                expected_mins_remaining = round((total_chunks_expected - (num_chunks_made + 1)) * secs_passed / 60.0, 2)
                print(" - Created chunk {}_{:03d} ({} secs, expected {} mins remaining)".format(prefix, num_chunks_made, secs_passed, expected_mins_remaining))
                local_time = time()

                current_KB_size = 0
                num_chunks_made += 1

        out_chunk_file.close()
        if compress:
            print(" - Compressing chunk {}...".format(out_path))
            os.system('xz {}'.format(out_path))
        
        secs_passed = round((time() - local_time), 2)
        print(" - Created FINAL chunk {}_{:03d} ({} secs)".format(prefix, num_chunks_made, secs_passed))
    return num_chunks_made






## OUTDATED????

# def write_chunk(lines, path, prefix, number, compress=True):
#     filepath = path + '/' + prefix + '_' + '{:03d}'.format(number) + '.json'
#     with open(filepath , 'w') as file:
#         for line in lines:
#             file.write(line + '\n')
#     if compress:
#         os.system('xz {}'.format(filepath))


# def chunk_json_file(filepath, out_dir, prefix, json_MB_chunk=100, compress=True):
#     current_KB_size = 0
#     lines = []
#     num_chunks_made = 0

#     total_size_KB = os.path.getsize(filepath) / 1000.0
#     total_chunks_expected = math.ceil(total_size_KB / (json_MB_chunk * 1000.0))

#     print(" - {} expected to chunk into  {} (+/- 1) files".format(filepath, total_chunks_expected))
#     local_time = time()

#     with open(filepath, 'r') as f:
#         for line in f:
#             bytes_size = utf8len(line)
#             lines.append(line)
#             current_KB_size += (bytes_size / 1000.0)

#             if current_KB_size >= json_MB_chunk * 1000:
#                 write_chunk(lines, out_dir, prefix, num_chunks_made, compress)
#                 current_KB_size = 0
#                 lines = []

#                 secs_passed = round((time() - local_time), 2)
#                 expected_mins_remaining = round((total_chunks_expected - (num_chunks_made + 1)) * secs_passed / 60.0, 2)
#                 print(" - Created chunk {}_{:03d} ({} secs, expected {} mins remaining)".format(prefix, num_chunks_made, secs_passed, expected_mins_remaining))
#                 local_time = time()

#                 num_chunks_made += 1
#     return num_chunks_made


def find_xz_files_above_size(folderpath, xz_MB_min_size=150):
    filenames = list(filter(lambda x: x.endswith('.xz') and ((os.path.getsize(folderpath + '/' + x) / 1000.0) > (xz_MB_min_size * 1000.0)), os.listdir(folderpath)))
    return filenames


FOLDER = './test_json'


if __name__ == '__main__':
    files = find_xz_files_above_size(FOLDER, xz_MB_min_size=150)

    print("Found {} files to chunk".format(len(files)))

    total_time = time()

    for index, file in enumerate(files):
        print("Chunking {} ({}/{})\n - Extracting file to json...".format(file, index + 1, len(files)))
        local_time = time()

        os.system('unxz {}'.format(FOLDER + '/' +file))

        print(" - Extracted xz file ({} secs)".format(round((time() - local_time), 2)))

        file_prefix = file.split('.')[0]
        json_path = FOLDER + '/' + file_prefix + '.json'

        num_chunks = chunk_json_file_write_while_going(json_path, FOLDER, file_prefix, json_MB_chunk=200)

        os.remove(json_path)

        print(" - Split {} into {} chunks ({} secs)\n".format(file, num_chunks, round((time() - local_time), 2)))

    print("Complete. ({} secs)".format(round((time() - total_time), 2)))