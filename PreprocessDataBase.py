
import os
from time import time

import pandas as pd

# FOLDER_PATH = './../../core.ac.uk/datasets/core_2018-03-01_metadata'
FOLDER_PATH = './test_json'


filenames = list(filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH)))


print('{} Total Files to process...\n'.format(len(filenames)))

total_time = time()

total_kept = 0
total_loaded = 0

for index, filename in enumerate(filenames):
    local_time = time()


    print('({}/{}) Processing {}'.format(index + 1, len(filenames), filename))


    in_path = FOLDER_PATH + '/' + filename

    df = pd.read_json(in_path, lines=True, compression={'method':'xz'})

    initial_num_docs = df.shape[0]
    total_loaded += initial_num_docs

    df = df[['doi', 'title', 'authors', 'datePublished', 'abstract', 'publisher', 'journals', 'topics']]

    df = df.dropna(subset=['doi', 'title', 'abstract']) # drop all rows where the doi or title is None

    # filter out abstracts with less than 5 words.
    abstract_mask = [True if x is not None and len(x.split()) > 5 else False for x in df['abstract']]
    df = df[abstract_mask]

    # language must be english or None (None is almost half of the papers)
    lang_mask = [True if x is None or 'english' == x['name'].lower() else False for x in df['language']]
    df = df[lang_mask]

    # filter to be only journal articles as subject
    journal_mask = [True if 'journal article' in str(x).lower() else False for x in df['subjects']]
    df = df[journal_mask]

    df['citation'] = '' #TODO: make citation

    df['json'] = df.apply(pd.DataFrame.to_json, axis=1)

    final_num_docs = df.shape[0]
    total_kept += final_num_docs

    file_prefix = filename.split('.')[0]
    out_path = FOLDER_PATH + '/' + file_prefix + '.json'

    if df.shape[0] > 0:
        with open(out_path, 'w') as file:
            for json_line in df['json']:
                file.write(json_line + '\n')
    
    os.remove(in_path)

    print(' - {}% docs kept ({} / {})'.format(round(100.0 * final_num_docs / initial_num_docs, 2), final_num_docs, initial_num_docs))

    print('Finished in {} secs (Total Time: {} mins)\n'.format(round((time() - total_time), 2), round((time() - total_time) / 60, 2)))


print('\nTotal Percent Docs Kept: {}% ({} / {})'.format(round(100.0 * total_kept / total_loaded, 2), total_kept, total_loaded))
print('Total Time: {} mins\n'.format(round((time() - total_time) / 60, 2)))
