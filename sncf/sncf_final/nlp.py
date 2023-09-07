import pickle
import spacy
import json
from collections import OrderedDict
import numpy as np


def nlp_predict(string):
    with open('./sncf_final/models/svm_model.pkl', 'rb') as f:
        model = pickle.load(f)
    array = []
    array.append(string)
    keywords = labelling_keywords(array)
    print('WORDS: ', keywords[0])
    print('WORDS: ', keywords[1])
    print('WORDS: ', keywords[2])
    test_features = np.array([[len(keywords[0]), keywords[0][0].count("de depart"), keywords[0][0].count("aller-retour"), keywords[0][0].count("Trajet de"), keywords[0][0].count("à destination")]])
    print('SENT TO MODEL:', test_features)
    prediction = model.predict(test_features)
    print('PREDICTION:', prediction)
    return prediction, keywords[1], keywords[2]

list_of_frequent_words = ["aller", "retour", "à", "trajet"]
pos_to_replace = ["NOUN", "PROPN"]
def labelling_keywords(sentences):
    filtered_sentences = []
    nlp = spacy.load("fr_core_news_lg")
    corpus = nlp.pipe(sentences)
    start = ""
    end = ""
    for idx, doc in enumerate(corpus):
        sentence = ""
        doc_ents = OrderedDict()
        # for ent in doc.ents:
        #     doc_key = ent.text
        #     # print(f"{doc_key}:{ent.label_}")
        
        for token in doc:
            if token.text in nlp.vocab:

                # print(f"{idx} - {token.text}: {token.pos_}")
                if (token.text.lower() not in list_of_frequent_words) :
                    #print(doc[token.i].text.lower().strip())
                    if token.text.lower() == "de" and doc[token.i-1].text.lower().strip() != "gare" and not "depart" in sentence:
                        sentence += f" {token.text.lower().strip()} "
                        if doc[token.i+1].pos_ in pos_to_replace:
                            sentence += "depart"
                            start = doc[token.i+1]
                        else:
                            sentence += f' {token.text.lower().strip()}'
                    elif doc[token.i-1].text.lower().strip() == "à" and token.pos_ in pos_to_replace:
                        
                        end = doc[token.i]
                        sentence += " destination"
                    elif (doc[token.i-1].text.lower().strip() == "de" and doc[token.i-2].text.lower().strip() != "gare") :
                        sentence += ""
                    elif (doc[token.i-1].text.lower().strip() == "-"):
                        sentence += ""
                    elif token.text.lower().strip() == "-":
                        sentence += ""
                    elif (token.text.lower() == "de" and doc[token.i-1].text.lower().strip() == "gare"):
                        sentence += ""
                    else:
                        sentence += f' {token.text.lower().strip()}'
                else:
                    sentence += f' {token.text.lower().strip()}'
        # print(words_filtered)

        
        filtered_sentences.append(sentence)
    return filtered_sentences, start, end
        