# from glob import glob
# from pathlib import Path
# from tqdm import tqdm
# all_f = glob('UD_corpora/*.conllu')
# with open('ud_corpora_gold.conllu', 'w') as gold:
#     for f in tqdm(all_f):
#         all_sents = Path(f).read_text().strip().split('\n\n')
#         for sent in all_sents:
#             if '# gold_annotation = True' in sent:
#                 gold.write(f'{sent}\n\n')

import subprocess, re, difflib
from collections import Counter
from pathlib import Path
from collections import defaultdict

def read_conllu(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        sentence_data = {
            'metadata': {},
            'tokens': []
        }
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                # Metadata line
                if '=' in line:
                    key, value = line[2:].split('=', 1)
                    sentence_data['metadata'][key.strip()] = value.strip()
            elif line == "":
                # Sentence finished
                if sentence_data['tokens']:  # Only add if there's content
                    data.append(sentence_data)
                sentence_data = {
                    'metadata': {},
                    'tokens': []
                }
            else:
                # Token line
                # if '-' not in line.split('\t')[0]:  # Skip multiword token lines (e.g., 6-7)
                if True:
                    parts = line.split('\t')
                    token_info = {
                        'id': parts[0],
                        'form': parts[1],
                        'lemma': parts[2],
                        'upos': parts[3],
                        'xpos': parts[4],
                        'feats': parts[5],
                        'head': parts[6],
                        'deprel': parts[7],
                        'deps': parts[8],
                        'misc': parts[9],
                    }
                    sentence_data['tokens'].append(token_info)
        # Catch last sentence if file doesn't end with newline
        if sentence_data['tokens']:
            data.append(sentence_data)
    return data

def write_conllu(conllu_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for sentence in conllu_data:
            # 写元数据
            for key, value in sentence['metadata'].items():
                f.write(f"# {key} = {value}\n")
            # 写 token 行
            for token in sentence['tokens']:
                fields = [
                    token['id'],
                    token['form'],
                    token['lemma'],
                    token['upos'],
                    token['xpos'],
                    token['feats'],
                    token['head'],
                    token['deprel'],
                    token['deps'],
                    token['misc']
                ]
                f.write('\t'.join(fields) + '\n')
            f.write('\n')

# file_path = "Roman_Weist_eud_gold.conllu"

# data = read_conllu(file_path)
# i = 0
# for d in data:
#     for tokens in d['tokens']:
#         if any(label in tokens['deprel'] and label in tokens['deps'] for label in ["reparandum:", "compound:svc"]):

#             i += 1
#             parts = tokens['deps'].split(':')
#             tokens["deprel"] =  parts[1]
#             if  tokens["misc"] != "SpaceAfter=No":
#                 tokens["misc"] = parts[-1]
#             tokens["deps"] = f"{parts[0]}:{parts[1]}"
# print(i)
# write_conllu(data, file_path)


def error_analysis(file_name):

    with open(file_name, "r", encoding="utf-8") as f:
        result = subprocess.run(
            ['python', 'tools/validate.py', '--lang', 'en', '--max-err=0'],
            stdin=f,
            capture_output=True,
            text=True
        )

    with open("error_log.txt", "a", encoding="utf-8") as error_file:
        error_file.write(result.stderr)


# input_folder_path = Path("UD-CHILDES/UD-CHILDES_gold")

# file_names = [f.name for f in input_folder_path.iterdir() if f.is_file()]

# for f in file_names:
#     if f != ".DS_Store":

#         print(f)

#         error_analysis(input_folder_path / f)

sa = 0

ret = defaultdict(int)

pattern = r"\[Line (\d+) Sent [^\]]+\]: (.*)"

unknown_edeprel = defaultdict(int)
advmod=[]

with open("error_log.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = re.match(pattern, line.strip())
        if not match:
            continue
        if 'SpaceAfter=No' in line:
            sa += 1
            continue

        elif 'Warning' in line:
            continue

        lines = line.split("]:")
        s = lines[-1].replace("\n", "")
        s = s.strip()
        #[L2 Metadata text-extra-chars] Extra characters at the end of the text attribute, not accounted for in the FORM fields: 'it's like a pretend animal.'
        if "fields:" in s:
            s = s.split("fields:")[0].strip() + " fields:"

        #[L2 Metadata text-form-mismatch] Mismatch between the text attribute and the FORM field. Form[6] is 'in' but text is 'what's in here Mummy?...'
        if "field." in s:
            s = s.split("field.")[0].strip() + " field."

        #[L3 Syntax leaf-aux-cop] 'aux' not expected to have children (5:will:aux --> 1:Well:discourse)
        if "children (" in s:
            s = s.split("children (")[0].strip() + " children"

        #[L4 Enhanced unknown-edeprel] Unknown enhanced relation type 'advcl:because_when' in '24:advcl:because_when'
        pattern_1 = r"^(\[.*?\] Unknown enhanced relation type) '([^']+)'"
        match_1 = re.match(pattern_1, s)
        if match_1:
            s = match_1.group(1)
            unknown_string = match_1.group(2)
            unknown_edeprel[unknown_string] += 1

        #  Xiiulin look at here!
        # [L1 Format overlapping-word-intervals] Range overlaps with others: 1-2: 2
        if "Range overlaps with others:" in s:
            s = s.split("Range overlaps with others:")[0].strip() + " Range overlaps with others:"

        # [L5 Morpho aux-lemma] 'eat' is not an auxiliary in language [en]: 1
        if "is not an auxiliary in language [en]" in s:
            s = "[L5 Morpho aux-lemma] '{{}}' is not an auxiliary in language [en]"

        # [L3 Syntax rel-upos-det] 'det' should be 'DET' or 'PRON' but it is 'PROPN' 'dis'
        if "'det' should be 'DET' or 'PRON' but it is" in s:
            advmod.append(s)
            s = "[L3 Syntax rel-upos-det] 'det' should be 'DET' or 'PRON' but it is 'PROPN' '{{}}'"

        if "[L3 Syntax punct-is-nonproj] Punctuation must not be attached non-projectively over nodes" in s:
            s = "[L3 Syntax punct-is-nonproj] Punctuation must not be attached non-projectively over nodes [{{}}]"

        # [L4 Syntax unknown-deprel] Unknown DEPREL label: 'LINK'
        if "Unknown DEPREL label" in s:
            s = "[L4 Syntax unknown-deprel] Unknown DEPREL label: '{{}}'"

        # [L2 Enhanced invalid-edeprel] Invalid enhanced relation type: '12:LINK'.
        if "Invalid enhanced relation type" in s :
            s = "[L2 Enhanced invalid-edeprel] Invalid enhanced relation type: '{{}}'"

        # [L5 Syntax cop-lemma] 'we' is not a copula in language [en]: 1
        if "is not a copula in language [en]" in s:
            s = "[L5 Syntax cop-lemma] '{{}}' is not a copula in language [en]"

        # [L3 Syntax upos-rel-punct] 'PUNCT' must be 'punct' but it is 'goeswith'
        if "'PUNCT' must be 'punct'" in s or "'punct' must be 'PUNCT'"in s:

            s = "[L3 Syntax upos-rel-punct] 'PUNCT' must be 'punct' but it is '{{}}'"

        # [L3 Syntax rel-upos-advmod] 'advmod' should be 'ADV' but it is 'SCONJ': 235
        if "'advmod' should be 'ADV'" in s:
            # advmod.append(s)
            s = "[L3 Syntax rel-upos-advmod] 'advmod' should be 'ADV' but it is '{{}}'"

        # [L3 Syntax rel-upos-aux] 'aux' should be 'AUX' but it is 'PART'
        if "'aux' should be 'AUX' but it is" in s:
            s = "[L3 Syntax rel-upos-aux] 'aux' should be 'AUX' but it is '{{}}'"

        # [L3 Syntax rel-upos-cop] 'cop' should be 'AUX' or 'PRON'/'DET' but it is 'VERB'
        if "'cop' should be 'AUX' or 'PRON'/'DET'" in s:

            s = "[L3 Syntax rel-upos-cop] 'cop' should be 'AUX' or 'PRON'/'DET' but it is '{{}}'"

        # [L3 Syntax rel-upos-case] 'case' should not be 'DET'
        if "'case' should not be" in s:
            s = "[L3 Syntax rel-upos-case] 'case' should not be '{{}}'"

        # [L3 Syntax rel-upos-expl] 'expl' should normally be 'PRON' but it is 'NOUN'
        if "'expl' should normally be 'PRON'" in s:
            s = "[L3 Syntax rel-upos-expl] 'expl' should normally be 'PRON' but it is '{{}}'"

        # [L3 Syntax rel-upos-mark] 'mark' should not be 'PRON'
        if "'mark' should not be" in s:
            s = "[L3 Syntax rel-upos-mark] 'mark' should not be '{{}}'"

        # [L3 Syntax rel-upos-nummod] 'nummod' should be 'NUM' but it is 'ADJ':
        if "'nummod' should be 'NUM'" in s:
            s = "[L3 Syntax rel-upos-nummod] 'nummod' should be 'NUM' but it is '{{}}'"


        # [L3 Morpho goeswith-lemma] The lemma of a 'goeswith'-connected word must be annotated only at the first part.
        # [L3 Morpho goeswith-upos] The UPOS tag of a 'goeswith'-connected word must be annotated only at the first part; the other parts must be tagged 'X'.
        # [L3 Morpho goeswith-missing-typo] Since the treebank has morphological features, 'Typo=Yes' must be used with 'goeswith' heads.
        # [L3 Syntax right-to-left-goeswith] Relation 'goeswith' must go left-to-right
        # [L3 Syntax goeswith-gap] Violation of guidelines: gaps in goeswith group [1, 2] != [
        # [L3 Syntax leaf-goeswith] 'goeswith' not expected to have children
        if "goeswith" in s:
            s = "goeswith"



        ret[s] += 1

ret = dict(sorted(ret.items(), key=lambda item: item[1], reverse = True))
print(len(ret))
print(sum(ret.values()) + sa)
print(sa)

print(unknown_edeprel)

with open("error_classification.txt", "w", encoding="utf-8") as f:
    for key, value in ret.items():
        f.write(f"{key}: {value}\n")

with open("unknown_enhanced_relation.txt", "w", encoding="utf-8") as f:
    for key, value in unknown_edeprel.items():
        f.write(f"{key}: {value}\n")
print(Counter(advmod).most_common(10))
