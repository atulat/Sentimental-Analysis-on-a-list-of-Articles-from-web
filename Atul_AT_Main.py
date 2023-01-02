# Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Preprocessing Function
def preprocessing(txt):
    # Tokenizing each word and special characters
    txt_tokens = word_tokenize(txt)
    print(txt_tokens)

    # Removing punctuations from the text
    no_punc_text = txt.translate(str.maketrans('', '', string.punctuation))

    # Removing URLs
    no_url_text = re.sub(r'http\S+', '', no_punc_text)

    # Tokenizing text after removing punctuations and URLs
    text_tokens = word_tokenize(no_url_text)
    print(text_tokens)

    # Removing Apostrophe
    text_nly = [word for word in text_tokens if word.isalnum()]

    # Stopwords package
    nltk.download('stopwords')

    # Lowering all the words
    lower_words = [Text.lower() for Text in text_nly]

    # Removing all the stopwords
    new_txt = []
    for i in lower_words:
        if i not in set(stopwords.words('english')):
            new_txt.append(i)

    # Removing -es -ed ending words
    syllable1 = [item for item in text_tokens if not item.endswith(("ed", "ing"))]

    # Accessing the list of Positive words
    positive = pd.read_table("/Users/atulat/Documents/20211030 Test Assignment/positive-words.txt")
    pos = []
    for i in positive['a+']:
        pos.append(i)

    # Accessing the list of Negative Words
    negative = pd.read_table("/Users/atulat/Documents/20211030 Test Assignment/negative-words.txt",
                             encoding="ISO-8859-1")
    neg = []
    for i in negative['2-faced']:
        neg.append(i)

    return (txt_tokens, text_nly, new_txt, syllable1, pos, neg)

# Calculation Function
def calculation(txt_tokens, text_nly, new_txt, syllable1, pos, neg):
    # Nullifying variables
    pos_sco = 0
    neg_sco = 0
    dot_cou = 0
    char_count = 0
    syllable_total_count = 0
    pronouns_count = 0
    complex_word_count = 0
    words_in_sentence = 0

    words_in_sentence_l1 = []
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    pronouns = [' I ', ' we ', ' my ', ' ours ', ' us ']

    # Calculating Positive and Negative Score
    for word in new_txt:
        if word in pos:
            pos_sco += 1
        elif word in neg:
            neg_sco += 1

    # Calculating Sentences
    for word in txt_tokens:
        if word != ".":
            words_in_sentence += 1
        else:
            words_in_sentence_l1.append(words_in_sentence)
            words_in_sentence = 0
            dot_cou += 1

    # Calculating Syllable
    for word in syllable1:
        syllable_count = 0
        for i in vowels:
            if i in word:
                syllable_count += word.count(i)
        syllable_total_count += syllable_count
        if syllable_count >> 2:
            complex_word_count += 1

    # Calculating Pronouns
    for word in pronouns:
        x = re.findall(word, txt)
        if len(x) >> 1:
            pronouns_count += len(x)

    # Calculating the fined text
    for char in text_nly:
        char_count += len(char)

    # Polarity Score
    pol_soc = (pos_sco - neg_sco) / ((pos_sco + neg_sco) + 0.000001)

    # Subjectivity Score
    sub_sco = (pos_sco - neg_sco) / (len(new_txt)) + 0.000001

    # Average Sentence Length
    avg_sent_len = len(txt_tokens) / dot_cou

    # Complex Word Percentage
    complex_pct = complex_word_count / len(new_txt)

    # Fog Index
    fog_index = 0.4 * (avg_sent_len + complex_pct)

    # Average Word Length
    avg_word_len = char_count / len(text_nly)

    return (
        pos_sco, neg_sco, pol_soc, sub_sco, avg_sent_len, dot_cou, complex_pct, complex_word_count, fog_index,
        avg_word_len,
        char_count, syllable_total_count, words_in_sentence_l1, pronouns_count)

#Reading the Excel File
df = pd.read_excel("/Users/atulat/Documents/20211030 Test Assignment/Input.xlsx")

# Creating a dataframe for Output
df_new = pd.DataFrame(columns=['URL','POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
       'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
       'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
       'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
       'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])

# Crating a new list name whole_list
whole_list = []

# Request Headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

# Accessing each URL
for url in df["URL"]:
    txt = ""

    # Accessing the content in the url
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Returning only text files from the class name 'td - post - content'
    for word in soup.find_all("div", {"class": "td-post-content"}):
        txt += word.text

    # Continuing the loop if the page is empty
    if txt == "":
        continue

    txt_tokens, text_nly, new_txt, syllable1, pos, neg = preprocessing(txt)

    pos_sco, neg_sco, pol_soc, sub_sco, avg_sent_len, dot_cou, complex_pct, complex_word_count, fog_index, avg_word_len, char_count, syllable_total_count, words_in_sentence_l1, pronouns_count = calculation(
        txt_tokens, text_nly, new_txt, syllable1, pos, neg)

    print("URL : ", url)
    print("Positive Score : ", pos_sco)
    print("Negative Score : ", neg_sco)
    print("Polarity Score : ", pol_soc)
    print("Subjectivity Score : ", sub_sco)
    print("Average Sentence Length : ", avg_sent_len)
    print("Percentage of Complex Words : ", complex_pct * 100)
    print("Fog Index : ", fog_index)
    print("Average Number of words per Sentence : ", np.mean(words_in_sentence_l1))
    print("Complex Word Count : ", complex_word_count)
    print("Word Count : ", len(text_nly))
    print("Syllable per word : ", syllable_total_count / len(syllable1))
    print("Personal Pronouns : ", pronouns_count)
    print("Average Word Length : ", avg_word_len)

    # Appending all the values into the list
    whole_list = [url, pos_sco, neg_sco, pol_soc, sub_sco, avg_sent_len, complex_pct * 100, fog_index,
                  np.mean(words_in_sentence_l1), complex_word_count,
                  len(text_nly), (syllable_total_count / len(syllable1)), pronouns_count, avg_word_len]

    # Adding the List into a Dataframe
    df_new.loc[len(df_new)] = whole_list

df_new.to_excel("/Users/atulat/Documents/Output.xlsx")
print(df_new)



