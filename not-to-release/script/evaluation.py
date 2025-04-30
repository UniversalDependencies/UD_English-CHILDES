import stanza
from conllu import parse
from conllu import TokenList
from tqdm import tqdm
from pathlib import Path
from glob import glob
from pathlib import Path
stanza.download("en")
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos, lemma,depparse',tokenize_pretokenized=True)
with open('gold_all.conllu', 'w') as all_g:
    ag=glob('corrected_gold/*.conllu')
    for conllu in ag:
        gold_text = Path(conllu).read_text().strip()
        all_g.write(gold_text)
        all_g.write('\n\n')

gold = Path('gold_all.conllu').read_text().strip().split('\n\n')
with open('stanza_pred.conllu', 'w') as pred:
    for sent in tqdm(gold):
        parsed = [x['form'] for x in parse(sent)[0] if '-' not in str(x['id'])]
        doc = nlp([parsed])

        for i, sentence in enumerate(doc.sentences):
            sentence_reform = ' '.join([token.text for token in sentence.words])
            pred.write(f'#sent = {sentence_reform}\n')
            for token in sentence.words:
                # print(f'{token.id}\t{token.text}\t_\t{token.upos}\t_\t_\t{token.head}\t{token.deprel}\t_\n')
                pred.write(f'{token.id}\t{token.text}\t_\t{token.upos}\t_\t_\t{token.head}\t{token.deprel}\t_\t_\n')
            pred.write('\n')
