from datetime import datetime

from article_crawler import crawl_rankings
from summarizer import test_summarize

if __name__ == "__main__":
    file_name = f"./crawledData{str(datetime.today().date()).replace('-', '')}.tsv"
    #crawl_rankings(file_name)
    test_summarize(file_name)