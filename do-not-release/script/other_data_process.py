from conllu import parse
from glob import glob
from pathlib import Path
import stanza
import pandas as pd
import argparse
from tqdm import tqdm
from conllu.models import TokenList



parser = argparse.ArgumentParser(
        prog='parse CHILDES',
        description='Parse CHILDES data')
parser.add_argument('child_folder',
                        help='The name of the folder that contains CHILDES data')
parser.add_argument('child_csv',
                        help='The name of the csv file that contains the corresponding CHILDES data')

args = parser.parse_args()
folder = args.child_folder
csv_name = args.child_csv


stanza.download("en")
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos, lemma,depparse')
children_path = glob(f'{folder}/*')
merged = {}
child_name = children_path[0].split('/')[1]
for p in tqdm(children_path):
    child_text = Path(p).read_text().strip().split('\n\n')
    for ch in child_text:
        parsed_text = parse(ch)
        text = ''.join([x['form'] for x in parsed_text[0]])
        merged[text] = parsed_text[0]



kuc = pd.read_csv(f'{csv_name}.csv').dropna(subset=['gloss']).to_dict('records')
misc_end = {'SpaceAfter': 'No'}
kuc_sent = {''.join(x['gloss'].split()): x for x in kuc}
with open(f'{child_name}.conllu', 'w') as corpus:
    for sent, infor in tqdm(kuc_sent.items()):
        concat_sent = ''.join(sent.split())
        unconcat_sent = infor['gloss']
        tokenized_sent = unconcat_sent.split()
        preprocessed_sent = unconcat_sent.replace('_', ' ')
        # preprocessed_sent = preprocessed_sent.replace("'", " '")
        if kuc_sent[concat_sent]['type'] == 'question':
            punct = '?'
        elif kuc_sent[concat_sent]['type'] == 'imperative_emphatic':
            punct = '!'
        elif kuc_sent[concat_sent]['type'] == 'declarative':
            punct = '.'
        else:
            punct = '.'
        preprocessed_sent = preprocessed_sent[0].upper()+preprocessed_sent[1:]+punct
        if concat_sent in merged:
            mwt_mannual = [{}]
            span_loc_mannual = []
            parses = merged[concat_sent]
            parses.metadata = {'text': preprocessed_sent,  'childes_toks': unconcat_sent,'sent_id': kuc_sent[concat_sent]['id'], 'corpus_name': kuc_sent[concat_sent]['corpus_name'], 'speaker_role': kuc_sent[concat_sent]['speaker_role'],
                               'speaker_gender': kuc_sent[concat_sent]['target_child_sex'], 'speaker_age': kuc_sent[concat_sent]['target_child_age'],
                               'type': kuc_sent[concat_sent]['type'], 'gold_annotation': 'True'}
            root_id = [k for k, p in enumerate(parses) if parses[k]['deprel']=='root'][0]

            auto_parse = nlp(unconcat_sent).sentences[0]
            if len(auto_parse.words) == len(parses):
                for kk in range(len(parses)):
                    if parses[kk]['form']!=auto_parse.words[kk].parent.text:
                        if auto_parse.words[kk].parent.text not in mwt_mannual[-1]:
                            mwt_mannual.append({auto_parse.words[kk].parent.text : [parses[kk]['id']]})
                        elif auto_parse.words[kk].parent.text in mwt_mannual[-1] and mwt_mannual[-1][auto_parse.words[kk].parent.text][-1]+1 ==parses[kk]['id']:
                            mwt_mannual[-1][auto_parse.words[kk].parent.text].append(parses[kk]['id'])
                        else:
                            # print(unconcat_sent)
                            mwt_mannual.append({auto_parse.words[kk].parent.text : [parses[kk]['id']]})

            for j in range(len(parses)):
                span_loc_mannual.append(parses[j]['id'])

                if j==0:
                    parses[j]['form'] = parses[j]['form'][0].upper()+parses[j]['form'][1:]
                if j==len(parses)-1:
                    parses[j]['misc'] = misc_end
                else:
                    parses[j]['misc'] = '_'
                parses[j]['deps'] = str(parses[j]['head'])+':'+parses[j]['deprel']
            parses.append({'id': len(parses)+1, 'form': punct, 'lemma': punct, 'upos': 'PUNCT', 'xpos':	punct, 'feats': '_', 'head': root_id+1, 'deprel': 'punct', 	'deps': f'{str(root_id+1)}:punct', 'misc': '_'})
            for entry_m in mwt_mannual:
                if len(entry_m)>0:
                    span_m_s = sorted(entry_m.values())[0][0]
                    span_m_e =sorted(entry_m.values())[0][-1]
                    mw_m = list(entry_m.keys())[0]
                    start_position = span_loc_mannual.index(span_m_s)
                    if span_m_s==1:
                        mw_m = mw_m[0].upper()+mw_m[1:]
                    parses.insert(start_position,
                                       {'id': str(span_m_s) + '-' + str(span_m_e), 'form': mw_m, 'lemma': '_', 'upos': '_',
                                        'xpos': '_', 'feats': '_', 'head': '_', 'deprel': '_', 'deps': '_',
                                        'misc': '_'})
                    # parses[start_position+1]['misc'] = misc_end
                    span_loc_mannual.insert(start_position, str(span_m_s) + '-' + str(span_m_e))


        else:
            auto_parses = nlp(preprocessed_sent).sentences[0]
            sent_parses = []
            sent_span_loc = []
            mwt = [{}]
            for idx, parse in enumerate(auto_parses.words):
                parse_feats = parse.feats if parse.feats else '_'
                if parse.parent.text != parse.text:
                    if parse.parent.text not in mwt[-1]:
                        mwt.append({parse.parent.text:[parse.id]})
                    elif parse.parent.text in mwt[-1] and parse.id == mwt[-1][parse.parent.text][-1]+1:
                        mwt[-1][parse.parent.text].append(parse.id)
                    else:
                        # print(preprocessed_sent)
                        mwt.append({parse.parent.text:[parse.id]})

                if idx!=len(auto_parses.words)-2:
                    sent_span_loc.append(parse.id)
                    sent_parses.append({'id':parse.id, 'form':parse.text, 'lemma': parse.lemma, 'upos':parse.upos, 'xpos': parse.xpos, 'feats': parse_feats, 'head': parse.head, 'deprel': parse.deprel, 'deps': str(parse.head)+':'+parse.deprel, 'misc':'_'})
                else:
                    sent_span_loc.append(parse.id)
                    sent_parses.append({'id':parse.id, 'form':parse.text, 'lemma': parse.lemma, 'upos':parse.upos, 'xpos': parse.xpos, 'feats': parse_feats, 'head': parse.head, 'deprel': parse.deprel, 'deps': str(parse.head)+':'+parse.deprel, 'misc':misc_end})

            for entry in mwt:
                if len(entry)>0:
                    span_s = sorted(entry.values())[0][0]
                    span_e = sorted(entry.values())[0][-1]
                    mw = list(entry.keys())[0]
                    start_position = sent_span_loc.index(span_s)
                    if span_s==1:
                        mw = mw[0].upper()+mw[1:]
                    sent_parses.insert(start_position, {'id':str(span_s)+'-'+str(span_e), 'form': mw, 'lemma': '_', 'upos':'_', 'xpos': '_', 'feats': '_', 'head': '_', 'deprel': '_', 'deps': '_', 'misc':'_'})
                    # sent_parses[start_position+1]['misc'] = misc_end
                    sent_span_loc.insert(start_position, str(span_s)+'-'+str(span_e))

            parses = TokenList(sent_parses)
            parses.metadata = {'text': preprocessed_sent,  'childes_toks': unconcat_sent, 'sent_id': kuc_sent[concat_sent]['id'], 'corpus_name': kuc_sent[concat_sent]['corpus_name'],
                            'speaker_role': kuc_sent[concat_sent]['speaker_role'],
                               'speaker_gender': kuc_sent[concat_sent]['target_child_sex'], 'speaker_age': kuc_sent[concat_sent]['target_child_age'],
                               'type': kuc_sent[concat_sent]['type'], 'gold_annotation': 'False'}

        corpus.write(parses.serialize())






