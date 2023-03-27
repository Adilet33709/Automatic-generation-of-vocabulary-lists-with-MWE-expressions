## Automatic Generation of Vocabulary Lists with Multiword Expressions
This repository contains code and automatically generated vocabulary list presented in our paper "Automatic Generation of Vocabulary Lists with Multiword Expressions". The paper will be presented in MWE 2023 Workshop. 
Specifically, the Code folder has two parts. The first part contains codes to evaluate a vocabulary list in terms of study time, text comprehension metrics introduced in our paper. The second part contains code to automatically generate vocabulary list with MWEs. 
## Before your start
1. Put Cambridge graded texts, OneStopEnglishCorpus, WeeBit folders into Resources folder. Each file should be name as "i+file" where i ranges from 1 to number of files in a given level.
2. In order to evaluate vocabulary list, put an Excel file with name of vocabulary list into Resource section.
3. Put Pickard.xlsx file with automatically generated MWEs into Resources folder. This resouce can be obtained from [Github repository](https://github.com/Oddtwang/MWEs). Also put EFLlex.xlsx file containing MWEs in EFLlex list (https://central.uclouvain.be/cefrlex/efllex/) into Resources folder. 
4. If you want to use your own Gold MWEs list, put your Gold MWEs list in Gold.xlsx file into Resources folder.
5. get_single_lemmas.py, get_bigrams.py, get_trigrams.py in Codes/List_generation are used to generate files in Resouces/List generation. These files are used to generate vocabulary list.
