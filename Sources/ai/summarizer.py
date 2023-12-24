import os.path

import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from konlpy.tag import Hannanum
from keybert import KeyBERT
import pandas as pd

# https://huggingface.co/eenzeenee/t5-base-korean-summarization t5기반 한국어 문서 요약 모델을 사용하여 기사들의 요약문 추출
# 기사 10개씩 나누어서 요약하도록 설정
def get_summarize(articles):
    nltk.download('punkt')

    model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-base-korean-summarization').to('cuda')
    tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-base-korean-summarization')
    result = []

    for i in range(0, len(articles), 30):
        inputs = ["summarize: " + article for article in articles[i:min(i+30, len(articles))]]
        inputs = tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt", padding=True).to('cuda')
        output = model.generate(**inputs, num_beams=3, do_sample=True, min_length=10, max_length=100)
        decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)
        result += decoded_output

    return result


# 요약문에서 불용어가 아닌 명사만을 추출하여 키워드로 사용. keyword_dic에 {키워드: 포함하는 문장 번호의 리스트} 형식으로 데이터 저장
def get_keywords(articles):
    #key_model = KeyBERT()
    key_model = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')
    hannanum = Hannanum()
    keyword_dic = {}
    stop_words = {"등", "씨", "것", "여성", "혐의", "경찰", "서울", "한국", "긴급", "불쾌", "이탈리", "10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대", "분노", "한", "징역", "제", "남성", "사고", "평균", "대한민국"}
    keywords = [key_model.extract_keywords(article, keyphrase_ngram_range=(1,2), top_n=2) for article in articles]
    keywords = [k[0][0] + ' ' + k[1][0] for k in keywords]
    for i, summary in enumerate(keywords):
        words = set([word for word in hannanum.nouns(summary) if word not in stop_words])
        keywords[i] = words
        for word in words:
            if word in keyword_dic:
                keyword_dic[word].append(i)
            else:
                keyword_dic[word] = [i]
    return keywords, keyword_dic


def summerize_article(file_name, processed_file):
    if(os.path.isfile(processed_file)):
        df = pd.read_csv(processed_file, sep='\t')
        keyword_dic = {}
        for i, words in enumerate(df['키워드']):
            for word in set(words[1:-1].split(',')):
                word = word.strip().strip("'")
                if word in keyword_dic:
                    keyword_dic[word].append(i)
                else:
                    keyword_dic[word] = [i]
        return df, keyword_dic
    df = pd.read_csv(file_name, sep='\t')
    df['기사요약'] = get_summarize(df['기사본문'])
    print(1)
    df['키워드'], keywords_dict = get_keywords(df['기사본문'])
    df.to_csv(processed_file, index=False, sep="\t")
    return df, keywords_dict
