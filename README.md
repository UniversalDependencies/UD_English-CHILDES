# Summary

This repository contains Universal Dependencies (UD) trees for utterances from child–adult spoken interactions in English, drawn from [CHILDES](https://childes.talkbank.org/) transcripts.

# Introduction
This treebank is built based on three existing treebanks (details under [References](#references)).
We compile, harmonize, and manually correct major UD-style annotations of CHILDES data into a consistent, unified UD format,
resulting in a gold-standard treebank of 48K sentences and 236K tokens.
## Overall Statistics

| Child  | Corpus     | Child Age Range     | Gold Sents | Gold Toks |
|--------|------------|---------------------|------------|-----------|
| Laura  | Braunwald  | 1;3–7;0 (1;3–7;0)   | 4,622      | 21,079    |
| Adam   | Brown      | 1;6–5;2 (1;6–5;2)   | 16,736     | 84,643    |
| Eve    | Brown      | 1;6–5;1 (1;6–5;2)   | 2,207      | 8,497     |
| Abe    | Kuczaj     | 2;4–5;0 (2;4–5;0)   | 4,167      | 22,437    |
| Sarah  | Brown      | 1;6–5;2 (1;6–5;2)   | 5,347      | 23,233    |
| Lily   | Providence | 0;11–4;0 (0;11–4;0) | 1,499     | 6,337     |
| Naima  | Providence | 1;3–3;11 (0;11–4;0) | 2,534     | 14,360    |
| Violet | Providence | 0;11–4;0 (0;11–4;0) | 721       | 1,857     |
| Thomas | Thomas     | 2;0–4;11 (2;0–4;11) | 4,240     | 20,333    |
| Emma   | Weist      | 2;2–4;10 (2;1–5;0)  | 2,423      | 13,730    |
| Roman  | Weist      | 2;2–4;9 (2;1–5;0)   | 3,653      | 20,557    |
 |Overall| NA         | NA                  |48,183      |236,941|

## Train, dev, test split statistics

| split | Children  | Corpus | Gold Sents |
|-------|-----------|---------|------------|
| Train | Adam, Lily, Naima, Sarah, Roman, Laura, Abe | Brown, Providence, Weist, Kuczaj, Braunwald| 34,732     |
| Dev   | Adam, Lily, Naima, Sarah, Roman, Laura, Abe    | Brown, Providence, Weist, Kuczaj, Braunwald | 3,860      |
| Test  | Eve, Violet, Emma, Thomas| Brown, Providence, Weist, Thomas| 9,591      |


## Example
```
# sent_id = 24433               (normalized sentence ID across corpora; used to avoid collisions since some corpora share identical sentence IDs)
# original_sent_id = 1715344    (original sentence ID from the corpus, as assigned in CHILDES-R)
# childes_toks = a world of Easter   (original token string from CHILDES-R)
# child_name = Adam
# corpus_name = Brown
# gold_annotation = True
# speaker_age = 31.03           (speaker's age in months)
# speaker_gender = male         (child's gender)
# speaker_role = Mother         (speaker role in conversation)
# type = trail off              (sentence type annotation)
# text = A world of Easter.

```

# References

The creation of this unified resource is detailed in:

Xiulin Yang, Zhuoxuan Ju, Lanni Bu, Zoey Liu, Nathan Schneider (2025). [UD-English-CHILDES: A Collected Resource of Gold and Silver Universal Dependencies Trees for Child Language Interactions](https://arxiv.org/abs/2504.20304). arXiv preprint.

```
@misc{yang2025udenglishchildescollectedresourcegold,
      title={UD-English-CHILDES: A Collected Resource of Gold and Silver Universal Dependencies Trees for Child Language Interactions},
      author={Xiulin Yang and Zhuoxuan Ju and Lanni Bu and Zoey Liu and Nathan Schneider},
      year={2025},
      eprint={2504.20304},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2504.20304},
}
```

Earlier resources that were consolidated:

- [S+24] Paper: [Cross-linguistically Consistent Semantic and Syntactic Annotation of Child-directed Speech](https://link.springer.com/article/10.1007/s10579-024-09734-y) by Ida Szubert, Omri Abend, Nathan Schneider, Samuel Gibbon, Louis Mahon, Sharon Goldwater, and Mark Steedman
   - Data Source: [CHILDES_UD2LF_2](https://github.com/Lou1sM/CHILDES_UD2LF_2)
   - CHILDES corpus: Adam Corpus (from the Brown Corpus)
   - The dataset is built based on the preannotation of [High-accuracy Annotation and Parsing of CHILDES Transcripts](https://aclanthology.org/W07-0604.pdf)

- [LP21] Paper: [Dependency Parsing Evaluation for Low-resource Spontaneous Speech](https://aclanthology.org/2021.adaptnlp-1.16/) by Zoey Liu and Emily Prud’hommeaux.
   - Data Source: [Parsing_Speech](https://github.com/zoeyliu18/Parsing_Speech/tree/main)
   - CHILDES corpus: Eve Corpus (from the Brown corpus)

- [LP23] Paper: [Data-driven Parsing Evaluation for Child-Parent Interactions](https://aclanthology.org/2023.tacl-1.97.pdf) by Zoey Liu and Emily Prud’hommeaux
  - Source: [Spoken_Parsing](https://github.com/ufcompling/spoken_parsing)
  - CHILDES corpora:
     - *Abe_Kuczaj*
     - *Adam_Brown*
     - *Emma_Weist*
     - *Laura_Braunwald*
     - *Lily_Providence*
     - *Naima_Providence*
     - *Roman_Weist*
     - *Sarah_Brown*
     - *Thomas_Thomas*
     - *Violet_Providence*

# Acknowledgments

We acknowledge Ida Szubert, Omri Abend, Samuel Gibbon, Louis Mahon, Sharon Goldwater, Mark Steedman, and Emily Prud’hommeaux for their contributions to the original UD treebanking efforts. We also thank Brian MacWhinney for helpful discussions.


# Changelog

* 2025-05-15 v2.16
  * Initial release in Universal Dependencies.


<pre>
=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.16
License: CC BY-SA 4.0
Includes text: yes
Genre: spoken
Lemmas: automatic with corrections
UPOS: automatic with corrections
XPOS: automatic
Features: not available
Relations: manual native
Contributors: Yang, Xiulin; Ju, Zhuoxuan; Bu, Lanni; Liu, Zoey; Schneider, Nathan
Contributing: here
Contact: xy236@georgetown.edu
===============================================================================
</pre>
