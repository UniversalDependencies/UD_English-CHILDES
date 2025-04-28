# Summary

This repository contains the Universal Dependencies (UD) treebanks derived from CHILDES corpora. 

# Introduction
This treebank is built based on three existing treebanks (details in Source Section).
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


## Sources
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
## References

* (citation)


# Changelog

* 2025-05-15 v2.16
  * Initial release in Universal Dependencies.


<pre>
=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.16
License: CC BY-SA 4.0
Includes text: yes
Genre: grammar-examples
Lemmas: manual native
UPOS: manual native
XPOS: not available
Features: manual native
Relations: manual native
Contributors: Yang, Xiulin
Contributing: here
Contact: xy236@georgetown.edu
===============================================================================
</pre>
