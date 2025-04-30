from pathlib import Path
import re

adam_path = 'adam_udv2_official.conllu'
adam_sents = Path(adam_path).read_text().strip().split('\n\n')

with open('adam.udv2.conllu', 'w') as f:
    for i, sent in enumerate(adam_sents):
        sent_lines = []
        for j, l in enumerate(sent.split('\n')):
            if '~' in l:
                l = re.sub('~', '', l)
                be_id = int(l.split()[0])
                prev_id = be_id -1
                abbre_id = f'{str(prev_id)}-{str(be_id)}'
                if int(prev_id)==1:
                    abbre_text = sent.split('\n')[j-1].split()[1][0].upper()+sent.split('\n')[j-1].split()[1][1:]+l.split()[1]

                else:
                    abbre_text = sent.split('\n')[j-1].split()[1]+l.split()[1]
                if j == len(sent.split('\n'))-2:
                    sent_lines.insert(j - 3, f'{abbre_id}\t{abbre_text}\t_\t_\t_\t_\t_\t_\t_\tSpaceAfter=No')
                else:
                    sent_lines.insert(j-3, f'{abbre_id}\t{abbre_text}\t_\t_\t_\t_\t_\t_\t_\t_')
                l = '\t'.join(l.split('\t')[:-2]) + '\t_\t' +l.split('\t')[-1]
                l = '\t'.join(l.split('\t')[:5]) + '\t_\t' + '\t'.join(l.split('\t')[6:])
            sent_lines.append(l)
        to_write_sent = '\n'.join(sent_lines)
        f.write(f'{to_write_sent}\n\n')

