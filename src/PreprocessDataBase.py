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
        abstract_mask = [True if x is not None and len(str(x)) > 500 else False for x in df['abstract']]
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
        total_time = time()
        for _, row in df.iterrows():
            embeddings.append(VecDoc(embedding=embedding_func(row['title'], row['abstract'], row['topics']), text="{}\n\n{}".format(row['citation'], row['abstract'])))
            count += 1
            elapsed_time = time() - total_time
            print("Processed {}/{}, {} minutes remaining".format(count, df.shape[0], round((elapsed_time / count) * (df.shape[0] - count + 0.00001) / 60, 2)))

    del df
    gc.collect()

    return embeddings
