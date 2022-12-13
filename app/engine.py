import nltk
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
import math
from gensim.summarization.summarizer import summarize
from rake_nltk import Rake
nltk.download('stopwords')

text = ""
result = ""

essay_str = ""
keywords_str = ""
summarize_str = ""

def get_text(text_name):
    global text
    with open(text_name, encoding='utf-8') as file:
        text = file.read()

def extract_keywords_from(text):
    r = Rake(max_length=5)
    r.extract_keywords_from_text(text)
    return ', '.join(r.get_ranked_phrases()[:5])

def get_essay(text):
    sentences = []
    for sentence in nltk.sent_tokenize(text):
        terms = []
        for term in nltk.word_tokenize(sentence):
            if term not in punctuation and term not in stopwords.words('russian') and term not in stopwords.words('german'):
                terms.append(term)
        sentences.append(terms)
    scores = []
    for sentence in sentences:
        score = 0
        for term in sentence:
            score += ((sentence.count(term)/len(sentence)) * 0.5 * (1+((sentence.count(term)/len(sentence))/(max_freq(sentence))))*math.log(len(sentences)/term_count(term, sentences)))
        scores.append(score)
    essay = ""
    for _ in range(int(len(sentences)/3)):
        current_max = max(scores)
        for i in range(len(scores)-1):
            if scores[i] == current_max:
                essay += nltk.sent_tokenize(text)[i]
                scores.remove(current_max)
                break
    return essay

def max_freq(sentence):
    result = 0
    for term in sentence:
        result = max(result,sentence.count(term))
    return result/len(sentence)

def term_count(term, sentences):
    result = 0
    for sentence in sentences:
        if term in sentence:
            result+=1
    return result

def print_result():
    global result
    global essay_str
    global keywords_str
    global summarize_str
    result = ""

    result += "========= Эссе по тексту: =========\n"
    essay_str = get_essay(text)
    result += essay_str
    result += "\n\n========= Подведение итогов: =========\n"
    summarize_str = summarize(text)
    result += summarize_str
    result += "\n\n========= Ключевые слова: =========\n"
    keywords_str = extract_keywords_from(text)
    result += keywords_str

def save_result():
    file = open('result.txt', 'w', encoding="utf8")
    file.write(result)
    file.close()

def run_logic(file_name):
    get_text(file_name)
    print_result()
    save_result()
    return essay_str, summarize_str, keywords_str
