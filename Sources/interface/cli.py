import os, platform


class CLI():

    def __init__(self, df, keywords_dict):
        self.df = df
        self.keywords_dict = keywords_dict
        self.system = platform.system()

    def run(self):
        self.print_keywords()

    def print_keywords(self):
        keywords = sorted(self.keywords_dict.keys(), key=lambda x: -len(self.keywords_dict[x]))
        keywords_set = set(keywords)
        n = 0  # n번부터 10개의 키워드를 보여줌
        while True:
            self.clear()
            print("------------------------------------------------------------")
            print("-----        현재 기사에서 많이 언급되는 키워드        -----")
            print("------------------------------------------------------------")
            print("-----                이전 10개 보기: b                 -----")
            print("-----                다음 10개 보기: n                 -----")
            print("-----    키워드가 등장한 기사 보기: 번호 or 키워드     -----")
            print("-----          프로그램 종료: exit or ctrl+c           -----")
            print("------------------------------------------------------------")
            print()
            for i, keyword in enumerate(keywords[n:n + 10]):
                print(f'{n + i}. {keyword}')
            print()
            while True:
                try:
                    command = input(">>")
                except:
                    break
                if command == "b":
                    if n - 10 >= 0:
                        n -= 10
                        break
                    else:
                        print("첫 페이지입니다. 다른 명령어를 입력해주세요.")
                        continue
                elif command == "n":
                    if n + 10 < len(keywords) - 1:
                        n += 10
                        break
                    else:
                        print("마지막 페이지입니다. 다른 명령어를 입력해주세요.")
                        continue
                elif command == "exit" or command == "quit":
                    return
                elif command.isdecimal() and (keyword_num := int(command)) < len(keywords):
                    self.print_titles(keywords[keyword_num])
                    break
                elif command.isalnum() and command in keywords_set:
                    self.print_titles(command)
                    break
                else:
                    print("올바르지 않은 명령어입니다. 명령어를 다시 확인해주세요.")

    def print_titles(self, keyword):
        n = 0  # n번부터 5개의 기사 정보(제목, 언론사, 요약문)를 출력해줌
        article_nums = self.keywords_dict[keyword]
        while True:
            self.clear()
            print("------------------------------------------------------------")
            print(f"-----        키워드 '{keyword}' 가 언급된 기사         -----")
            print("------------------------------------------------------------")
            print("-----                 이전 5개 보기: b                 -----")
            print("-----                 다음 5개 보기: n                 -----")
            print("-----          기사 전문 보기: 기사 번호 입력          -----")
            print("-----           키워드 보기로 돌아가기: exit           -----")
            print("------------------------------------------------------------")
            print()
            for article_num in article_nums[n:n + 5]:
                article = self.df.loc[article_num]
                print(f"{article_num}번 기사")
                print(f"{article['기사제목']}\t{article['언론사명']}")
                print(f"{article['기사요약']}")
                print()
            while True:
                try:
                    command = input(">>")
                except:
                    break
                if command == "b":
                    if n - 5 >= 0:
                        n -= 5
                        break
                    else:
                        print("첫 페이지입니다. 다른 명령어를 입력해주세요.")
                        continue
                elif command == "n":
                    if n + 5 < len(article_nums) - 1:
                        n += 5
                        break
                    else:
                        print("마지막 페이지입니다. 다른 명령어를 입력해주세요.")
                        continue
                elif command == "exit" or command == "quit":
                    return
                elif command.isdecimal() and (article_num := int(command)) in article_nums:
                    self.clear()
                    article = self.df.loc[article_num]
                    print(f'기사제목\t{article["기사제목"]}\n')
                    print(f'언론사명\t{article["언론사명"]}\n')
                    print(f'기사링크\t{article["기사링크"]}\n')
                    article_text = article["기사본문"].replace(".", ".\n")  # 가독성을 위해 마침표 뒤에 줄바꿈 추가
                    print(f'기사본문\n{article_text}\n')
                    print(f'키워드\t{article["키워드"]}\n')
                    input("엔터를 눌러 나가기>>")
                    break
                else:
                    print("올바르지 않은 명령어입니다. 명령어를 다시 확인해주세요.")

    def clear(self):  # os별 터미널 화면 초기화 명령어 사용. 코랩에서는 정상적으로 작동하지 않음.
        if self.system == 'Windows':
            os.system("cls")
        else:
            os.system("clear")
