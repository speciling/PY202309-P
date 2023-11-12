from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


# 주어진 링크의 html파일을 lxml로 파싱한 BeautifulSoup 객체를 반환하는 함수
def get_soup(link):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    head = {"user-agent": USER_AGENT}
    req = requests.get(link, headers=head)
    html = req.text
    soup = bs(html, "lxml")
    return soup


# 링크가 주어진 기사의 정보를 리스트로 만들어 반환하는 함수
# [기사제목, 기사링크, 기사본문, 댓글수] 형태로 반환
def crawl_article(article_link):
    soup = get_soup(article_link)

    title = soup.select_one("#title_area > span").text
    body_text = soup.select_one("#dic_area").text.strip().replace("\n", " ")

    # 자바스크립트로 정보를 가져오는지 html상에는 정보가 표시되지 않음
    # 셀레니움을 이용해야 할 것으로 보임
    comments_num = "0"

    return [title, article_link, body_text, comments_num]


# 네이버 뉴스의 랭킹뉴스 페이지에서 언론사별 조회수 상위 5개 기사의 정보를 수집하는 함수
# 각 기사에 대해 crawl_article 함수를 사용하여 기사 정보를 얻어오고, tsv파일에 저장
def crawl_rankings(file_name):
    rankings_link = "https://news.naver.com/main/ranking/popularDay.naver"
    soup = get_soup(rankings_link)
    rankingnews_boxes = soup.select(".rankingnews_box")  # 언론사별 랭킹 5위까지의 기사 정보가 담긴 박스들 선택

    with open(file_name, 'w', encoding="utf8") as fp:
        fp.write("언론사명\t기사제목\t기사링크\t기사본문\t댓글수\n")

        for box in rankingnews_boxes:
            company_name = box.select_one(".rankingnews_name").text
            articles = box.select("li")

            for i, article in enumerate(articles):
                try:
                    # 링크는 https://n.news.naver.com/article/언론사코드/기사번호?ntype=RANKGIN 형태
                    article_link = article.select_one(".list_title")["href"]
                    article_data = crawl_article(article_link)
                    fp.write(company_name + "\t" + "\t".join(article_data) + "\n")
                # 집계기준에 해당하는 기사가 없어 랭킹 5위까지 기사가 존재하지 않을 때
                except:
                    print(company_name, i+1, "번째 기사 수집 실패")


if __name__ == "__main__":
    file = f"./data{str(datetime.today().date()).replace('-', '')}.tsv"
    crawl_rankings(file)