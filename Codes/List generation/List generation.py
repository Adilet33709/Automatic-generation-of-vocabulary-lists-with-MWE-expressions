## Program that generates vocabulary list with MWEs

import spacy
import string
import pandas as pd
from collections import OrderedDict
from math import log10



gold_list = pd.read_excel("Gold.xlsx", header=None).iloc[:, 0].tolist()


## Function inputs list of dicts. Outputs cleander list of dicts by 
## POS, punctuation, removing "ve" or "s"
def clean_list_of_dicts(list_of_dicts):
    cleaned_list_of_dicts = []
    for dictionary in list_of_dicts:
        ## Remove words with specified POS
        POS_exclude = ["NUM", "PROPN", "PUNCT", "SPACE", "SYM", "X"]
        if dictionary["tag"] in POS_exclude:
            pass
        ## Remove if word len = 1 and it is in punctuation list
        elif any(c.isalpha() for c in dictionary["word"]) == False:
            pass
        ## Remove if word is either "'ve" or "'s"
        elif dictionary["word"] == "'ve" or dictionary["word"] == "'s":
            pass
        else:
            cleaned_list_of_dicts.append(dictionary)
    return cleaned_list_of_dicts

### Function that finds MWE's from the list of dicts and adds new key/value pair MWE and its value
### Gold list is list of MWE from EVP/GSE
def get_MWE(list_of_dicts, gold_list):
    output_list = list_of_dicts
    for i in range(len(list_of_dicts)-1):
        ## For lemmas
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] != "Remove") and (output_list[i+1]["MWE"] != "Remove"):
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = "Remove"
        ## For words
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] != "Remove") and (output_list[i+1]["MWE"] !=  "Remove"):
                    if output_list[i]["MWE"] == None and output_list[i+1]["MWE"] == None:
                        output_list[i]["MWE"] = MWE
                        output_list[i+1]["MWE"] = "Remove"
    return output_list

def get_trigram_MWE(list_of_dicts, gold_list):
    output_list = list_of_dicts
    for i in range(len(list_of_dicts)-2):
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"] + " " + list_of_dicts[i+2]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = "Remove"
                output_list[i+2]["MWE"] = "Remove"
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"] + " " + list_of_dicts[i+2]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = "Remove"
                    output_list[i+2]["MWE"] = "Remove"
    ##Include wildcard
    for i in range(len(list_of_dicts)-2):
        MWE = list_of_dicts[i]["lemma"] + " " + "wildcard" + " " + list_of_dicts[i+2]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = "Remove"
                output_list[i+2]["MWE"] = "Remove"
        else:
            MWE = list_of_dicts[i]["word"] + " " + "wildcard" + " " + list_of_dicts[i+2]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = "Remove"
                    output_list[i+2]["MWE"] = "Remove"
    return output_list




### Function that takes exam name and file_name in string format, POS=list of POS to exclude words 
# and outputs its lowercased lemmatized form in a form of a list
### Excluding POS
def text_to_list_excl_POS(level, file_name, corpora):
    # opening the file in read mode
    my_file = open("Resources/" +corpora+ "/" + level + "/" + file_name + ".txt", "r")
    # reading the file
    data = my_file.read()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(data)
    output_list = []
    for token in doc:
        output_dict = {}
        output_dict["word"] = token.text
        output_dict["lemma"] = token.lemma_
        output_dict["tag"] = token.pos_
        output_dict["MWE"] = None
        output_list.append(output_dict)
    my_file.close()
    output_list = clean_list_of_dicts(output_list)
    output_list = get_trigram_MWE(output_list, gold_list)
    output_list = get_MWE(output_list, gold_list)
    text_list = []
    for dictionary in output_list:
        if dictionary["MWE"] == None:
            text_list.append(dictionary["lemma"])
        elif dictionary["MWE"] == "Remove":
            pass
        else:
            text_list.append(dictionary["MWE"])
    ## Lowercase all strings
    for i in range(len(text_list)):
        text_list[i] = text_list[i].lower()
    ## For int texts remove first word which shows level name.
    if level == "Int-Txt":
        text_list = text_list[1:]
    my_file.close()
    return text_list



### Function that takes exam name and returns nested list where each element is a list of words of a text exlcuding
### words with specified POS.
def texts_to_lists_excl_POS(level, corpora, folder_size):
    texts_list = []
    for i in range(folder_size):
        file_name = str(i+1) + "file"
        texts_list.append(text_to_list_excl_POS(level, file_name, corpora))
    return texts_list


### Get all lemmas as list
def combine_all_texts(levels, corpora, folder_size):
    all_words = []
    for level in levels:
        ## Get nested list for each exam
        x = texts_to_lists_excl_POS(level, corpora, folder_size)
        ## Open each list element of x and add them to all_words
        for i in range(len(x)):
            all_words += x[i]
    return all_words



## Function given list of percentages, it computes their variation coefficient and then dispersion
def get_dispersion_coefficient(list_of_percentages):
    mean = 0
    for percentage in list_of_percentages:
        mean += percentage / len(list_of_percentages)
    sum_squares = 0
    for percentage in list_of_percentages:
        sum_squares += (mean - percentage) ** 2
    sd = (sum_squares/ len(list_of_percentages)) ** 0.5
    dispersion_value = 1 - sd / mean * 1 / (len(list_of_percentages)-1) ** 0.5
    return dispersion_value



### Function that inputs word and outputs their percentages
def get_list_of_percentages(word):
    list_of_percentages = []
    list_of_percentages.append(OSE_ele.count(word) / len(OSE_ele))
    list_of_percentages.append(OSE_int.count(word) / len(OSE_int))
    list_of_percentages.append(OSE_adv.count(word) / len(OSE_adv))
    list_of_percentages.append(WB_l2.count(word) / len(WB_l2))
    list_of_percentages.append(WB_l3.count(word) / len(WB_l3))
    list_of_percentages.append(WB_l4.count(word) / len(WB_l4))
    list_of_percentages.append(WB_ks3.count(word) / len(WB_ks3))
    list_of_percentages.append(WB_gcse.count(word) / len(WB_gcse))
    assert len(list_of_percentages) == 8

    return list_of_percentages

### Function that inputs list of words and outputs list of dicts where key is word and value is Dispersion
def dispersion_calculator(list_of_words):
    list_of_dicts = []
    for word in list_of_words:
        new_dict = {}
        probability = all_lemmas.count(word) / len(all_lemmas)
        percentages = get_list_of_percentages(word)
        dispersion = get_dispersion_coefficient(percentages)
        new_dict["word"] = word
        new_dict["probability"] = probability
        new_dict["adjusted probability"] = probability * dispersion
        #new_dict["log prob"] = log10(probability * dispersion)
        list_of_dicts.append(new_dict)
    return list_of_dicts







## Upload all lemmas
OSE_ele = combine_all_texts(["Ele-Txt"], "OneStopEnglishCorpus", 189)
OSE_int = combine_all_texts(["Int-Txt"], "OneStopEnglishCorpus", 189)
OSE_adv = combine_all_texts(["Adv-Txt"], "OneStopEnglishCorpus", 189)
WB_l2 = combine_all_texts(["WRLevel2"], "WeeBit", 616)
WB_l3 = combine_all_texts(["WRLevel3"], "WeeBit", 616)
WB_l4 = combine_all_texts(["WRLevel4"], "WeeBit", 616)
WB_ks3 = combine_all_texts(["BitKS3"], "WeeBit", 616)
WB_gcse = combine_all_texts(["BitGCSE"], "WeeBit", 616)
all_lemmas = OSE_ele + OSE_int + OSE_adv + WB_l2 + WB_l3 + WB_l4 + WB_ks3 + WB_gcse
all_lemmas_filter = []

for word in all_lemmas:
    if word in all_lemmas_filter:
        pass
    else:
        all_lemmas_filter.append(word)


list_of_dicts = dispersion_calculator(all_lemmas_filter)





## Save to excel
pd.DataFrame(list_of_dicts).to_excel("Automatically generated list.xlsx", header=None)