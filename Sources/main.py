from datetime import datetime

from article_crawler import crawl_rankings

if __name__ == "__main__":
    file = f"./data{str(datetime.today().date()).replace('-', '')}.tsv"
    crawl_rankings(file)