import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from konlpy.tag import Hannanum

# https://huggingface.co/eenzeenee/t5-base-korean-summarization t5기반 한국어 문서 요약 모델을 사용하여 기사들의 요약문 추출
def summarize(articles):
    nltk.download('punkt')

    model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-base-korean-summarization')
    tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-base-korean-summarization')

    inputs = ["summarize: " + article for article in articles]
    inputs = tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt", padding=True)
    output = model.generate(**inputs, num_beams=3, do_sample=True, min_length=10, max_length=100)
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)
    return decoded_output


# 요약문에서 불용어가 아닌 명사만을 추출하여 키워드로 사용. keyword_dic에 {키워드: 포함하는 문장 번호의 리스트} 형식으로 데이터 저장
def get_keywords(summaries):
    hannanum = Hannanum()
    keyword_dic = {}
    stop_words = ["등", "씨", "것"]
    for i, summary in enumerate(summaries):
        words = set([word for word in hannanum.nouns(summary) if word not in stop_words])
        for word in words:
            if word in keyword_dic:
                keyword_dic[word].append(i)
            else:
                keyword_dic[word] = [i]
    return keyword_dic


def test_summarize(file_name):
    titles = []
    articles = []
    with open(file_name, 'r', encoding='utf8') as fp:
        for line in fp.readlines()[1:11]:
            line = line.split('\t')
            titles.append(line[1])
            articles.append(line[-1])
    summarized_sentences = summarize(articles)
    keywords_dict = get_keywords(summarized_sentences)
    print("----- 기사제목: 요약문 -----")
    for i in range(len(titles)):
        print(titles[i] + ": " + summarized_sentences[i])
    print()
    print("----- 키워드 목록 상위 10개 -----")
    for keyword in keywords_dict.keys()[:10]:
        print(keyword + ": " + str(keywords_dict[keyword]))