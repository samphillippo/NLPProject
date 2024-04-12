import gc
from time import time
import pandas as pd

from LocalVectorDB import VecDoc
from CitationGenerator import generate_citation


def process_file(filename, embedding_func):

    df = pd.read_json(filename, lines=True, compression={'method':'xz'})
    df = df.dropna(subset=['title']) # drop all rows where the title is None

    if df.shape[0] > 0:
        # filter out abstracts with less than 5 words.
        abstract_mask = [True if x is not None and len(str(x)) > 100 else False for x in df['abstract']]
        temp = df[abstract_mask]
        df = temp

    if df.shape[0] > 0:
        # language must be english or None (None is almost half of the papers)
        lang_mask = [True if x is None or (isinstance(x, dict) and 'english' == x['name'].lower()) or str(x) == 'nan' else False for x in df['language']]
        temp = df[lang_mask]
        df = temp

    embeddings = []

    if df.shape[0] > 0:
        print("Generating citations")
        df['citation'] = df.apply(generate_citation, axis=1)
        print("Generating embeddings")
        print("Documents to Process: {}".format(df.shape[0]))
        count = 0
        #AVERAGE TIME TAKEN: 0.03 min
        for _, row in df.iterrows():
            embeddings.append(VecDoc(embedding=embedding_func(row['title'], row['abstract'], row['topics']), text="{}\n\n{}".format(row['citation'], row['abstract'])))
            count += 1
            print("Processed {}/{}, {} minutes remaining".format(count, df.shape[0], round((df.shape[0] - count) * 0.03, 2)))

    del df
    gc.collect()

    return embeddings



# if __name__ == '__main__':
#     filenames = list(filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH)))
#     print('{} Total Files to process...\n'.format(len(filenames)))

#     total_time = time()

#     total_kept = 0
#     total_loaded = 0

#     dropped_missing_data = 0
#     dropped_abstract = 0
#     dropped_lang = 0

#     results = []
#     with tqdm(total=len(filenames)) as progress:
#         with ProcessPoolExecutor(max_workers=4, max_tasks_per_child=1) as executor:
#             # results = list(tqdm(executor.map(process_file, filenames), total=len(filenames)))
#             futures = [executor.submit(process_file, filename) for filename in filenames]
#             for future in as_completed(futures):
#                 result = future.result()
#                 total_loaded += result[0]
#                 total_kept += result[1]
#                 dropped_missing_data += result[2]
#                 dropped_abstract += result[3]
#                 dropped_abstract += result[4]
#                 progress.update()

#     if total_loaded == 0:
#         print('\nError: No data loaded...')
#     else:
#         print('\nTotal Files Processed: {}'.format(len(filenames)))
#         print('Total Percent Docs Kept: {}% ({} / {})'.format(round(100.0 * total_kept / total_loaded, 2), total_kept, total_loaded))
#         print('Docs Dropped Reasoning:\n - Missing Title: {}\n - Abstract length: {}\n - Language (Not English or None): {}'.format(dropped_missing_data, dropped_abstract, dropped_lang))
#     print('Total Time: {} mins\n'.format(round((time() - total_time) / 60, 2)))
