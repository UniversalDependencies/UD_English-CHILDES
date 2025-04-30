from pathlib import Path
from glob import glob
from tqdm import tqdm
import stanza
stanza.download("en")
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos, lemma,depparse',tokenize_pretokenized=True)

from conllu import parse_incr
with open('UD-CHILDES_gold/Brown_Eve_eud_gold_a.conllu', 'w') as final:
    data_file = open("UD-CHILDES_gold/Brown_Eve_eud_gold.conllu", "r", encoding="utf-8")
    parsed_sent = parse_incr(data_file)
    for sent in parsed_sent:
        tokenized_sent = [x['form'] for x in sent if '-'not in str(x['id'])]
        parsed = nlp([tokenized_sent])
        stanza_sent = parsed.sentences[0].words
        print(type(stanza_sent[0].id))
        print(stanza_sent[0].upos, stanza_sent[1].xpos)
        print([x.text for x in stanza_sent])
        w_id = 0
        for word in sent:
            if '-' not in str(word['id']):
                w_id+=1
                print(w_id)
                print([x.id for x in stanza_sent])
                word['upos']=[x.upos for x in stanza_sent if w_id==x.id][0]
                word['xpos']=[x.xpos for x in stanza_sent if w_id==x.id][0]
        final.write(sent.serialize())







    # sent=tokenlist.serialize()
    # final.write(sent)

# with open('UD-CHILDES_gold/Abe_kuczaj_eud_gold_r.conllu', 'w') as final:
#     data_file = Path("UD-CHILDES_gold/Abe_kuczaj_eud_gold.conllu").read_text().strip().split('\n')
#     for line in tqdm(data_file):
#         if len(line.split('\t'))==10:
#             if '-' in line.split('\t')[0] and line[-1]=='_':
#                 line = line[:-1]+'SpaceAfter=No'
#         final.write(line)
#         final.write('\n')

# all_files = glob('UD_corpora/Brown_Eve_eud.conllu')
# for file in all_files:
#     name = Path(file).stem
#     with open(f'UD-CHILDES_gold/{name}_gold.conllu', 'w') as gold, open(f'UD-CHILDES_silver/{name}_silver.conllu', 'w') as silver:
#         conllu_file = Path(file).read_text().strip().split('\n\n')
#         for sent in tqdm(conllu_file):
#             if '# gold_annotation = True' in sent:
#                 gold.write(sent)
#                 gold.write('\n\n')
#             else:
#                 silver.write(sent)
#                 silver.write('\n\n')


