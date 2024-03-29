import os
import gc
from time import time
from concurrent.futures import ProcessPoolExecutor, as_completed


from tqdm import tqdm
import pandas as pd

from CitationGenerator import generate_citation

# FOLDER_PATH = './../../core.ac.uk/datasets/core_2018-03-01_metadata'
FOLDER_PATH = './test_json'


def process_file(filename):
    local_time = time()

    # print('Processing {}'.format(filename))
    in_path = FOLDER_PATH + '/' + filename

    df = pd.read_json(in_path, lines=True, compression={'method':'xz'})

    initial_num_docs = df.shape[0]

    df = df.dropna(subset=['title']) # drop all rows where the title is None
    tot_dropped_missing_data = (initial_num_docs - df.shape[0])
    
    tot_dropped_abstract = 0
    if df.shape[0] > 0:
        # filter out abstracts with less than 5 words.
        abstract_mask = [True if x is not None and len(str(x).split()) > 5 else False for x in df['abstract']]
        temp = df[abstract_mask]
        tot_dropped_abstract = df.shape[0] - temp.shape[0]
        df = temp

    tot_dropped_lang = 0
    if df.shape[0] > 0:
        # language must be english or None (None is almost half of the papers)
        lang_mask = [True if x is None or (isinstance(x, dict) and 'english' == x['name'].lower()) or str(x) == 'nan' else False for x in df['language']]
        temp = df[lang_mask]
        tot_dropped_lang = df.shape[0] - temp.shape[0]
        df = temp
        
    json_values = []

    if df.shape[0] > 0:
        df['citation'] = df.apply(generate_citation, axis=1)
        df = df[['title', 'abstract', 'topics', 'citation']]
        json_values = [row.to_json() for _, row in df.iterrows()]

    final_num_docs = df.shape[0]

    file_prefix = filename.split('.')[0]
    out_path = FOLDER_PATH + '/' + file_prefix + '.json'

    if len(json_values) > 0:
        with open(out_path, 'w') as file:
            for json_line in json_values:
                file.write(json_line + '\n')
    
    os.remove(in_path)
    
    del df
    gc.collect()

    # print('Finished processing {} in {} secs\n - {}% docs kept ({} / {})\n'.format(filename, round((time() - local_time), 2), round(100.0 * final_num_docs / initial_num_docs, 2), final_num_docs, initial_num_docs))
    return (initial_num_docs, final_num_docs, tot_dropped_missing_data, tot_dropped_abstract, tot_dropped_lang)
    # END METHOD



if __name__ == '__main__':
    filenames = list(filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH)))
    print('{} Total Files to process...\n'.format(len(filenames)))

    total_time = time()

    total_kept = 0
    total_loaded = 0

    dropped_missing_data = 0
    dropped_abstract = 0
    dropped_lang = 0

    results = []
    with tqdm(total=len(filenames)) as progress:
        with ProcessPoolExecutor(max_workers=4, max_tasks_per_child=1) as executor:
            # results = list(tqdm(executor.map(process_file, filenames), total=len(filenames)))
            futures = [executor.submit(process_file, filename) for filename in filenames]
            for future in as_completed(futures):
                result = future.result()
                total_loaded += result[0]
                total_kept += result[1]
                dropped_missing_data += result[2]
                dropped_abstract += result[3]
                dropped_abstract += result[4]
                progress.update()
        # for file in filenames:
        #     result = process_file(file)
        #     total_loaded += result[0]
        #     total_kept += result[1]
        #     dropped_missing_data += result[2]
        #     dropped_abstract += result[3]
        #     dropped_abstract += result[4]
        #     progress.update()

    if total_loaded == 0:
        print('\nError: No data loaded...')
    else:
        print('\nTotal Files Processed: {}'.format(len(filenames)))
        print('Total Percent Docs Kept: {}% ({} / {})'.format(round(100.0 * total_kept / total_loaded, 2), total_kept, total_loaded))
        print('Docs Dropped Reasoning:\n - Missing Title: {}\n - Abstract length: {}\n - Language (Not English or None): {}'.format(dropped_missing_data, dropped_abstract, dropped_lang))
    print('Total Time: {} mins\n'.format(round((time() - total_time) / 60, 2)))
