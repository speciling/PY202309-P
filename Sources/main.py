from datetime import datetime

from crawler.article_crawler import crawl_rankings
from ai.summarizer import summerize_article
from interface.cli import CLI


def main():
    print("기사 크롤링중...")
    crawled_file = f"./crawledData{str(datetime.today().date()).replace('-', '')}.tsv"
    crawl_rankings(crawled_file)
    print("기사 크롤링 완료.")
    print("기사 요약, 키워드 추출중...")
    processed_file=f"./processedData{str(datetime.today().date()).replace('-', '')}.tsv"
    df, keywords_dict = summerize_article(crawled_file, processed_file)
    print("요약 및 키워드 추출 완료.")
    screen = CLI(df, keywords_dict)
    screen.run()


if __name__ == "__main__":
    main()