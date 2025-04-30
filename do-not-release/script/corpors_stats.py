from glob import glob
from conllu import parse
from pathlib import Path
data_path = glob('UD_corpora/*.conllu')
from tqdm import tqdm
from io import open
from conllu import parse_tree_incr

with open('corpus_stats.tsv', 'w') as corp_st:
    print('CORPUS NAME \t #GOLD EXP \t #GOLD TOKS \t #SILVER EXP \t #SILVER TOKS\n')
    for p in data_path:
        corpus_name = p.split('/')[-1].split('.')[0][:-4]
        gold_utterances=[]
        silver_utterances=[]
        sentences = open(p, "r", encoding="utf-8")
        for sent in tqdm(parse_tree_incr(sentences)):
            if 'gold_annotation' not in sent.metadata:
                gold_utterances.append(sent.metadata['text'])
                assert corpus_name =='Adam'
            elif sent.metadata['gold_annotation']=='True':
                gold_utterances.append(sent.metadata['text'])
            else:
                silver_utterances.append(sent.metadata['text'])

        gold_num = len(gold_utterances)
        gold_sum = sum([len(x.split()) for x in gold_utterances])
        silver_num = len(silver_utterances)
        silver_sum = sum([len(x.split()) for x in silver_utterances])

        corp_st.write(f'{corpus_name}\t{gold_num}\t{gold_sum}\t{silver_num}\t{silver_sum}\n')
