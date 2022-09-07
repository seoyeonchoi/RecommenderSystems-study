from tqdm import tqdm
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# parameters
driver_path = 'C:\\Users\\komac\\Desktop\\PythonWorkspace\\DSOB\\resources\\chromedriver95.exe'
# 각자 크롬 드라이버 경로

# get chromedriver

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(executable_path=driver_path, options=options)

# get links of each competition
page = browser.page_source
soup = BeautifulSoup(page, "html.parser")  # get HTML text

movieNums = [192150, 184318, 184311, 189150, 188472, 196051, 187323, 184517, 187322, 187348,
           185614, 190320, 191559, 99702, 187310, 194205, 191597, 189368, 204496, 190726,
           199860, 191637, 189124, 167569, 192620, 159074, 207523, 202903, 189075, 185293,
           184518, 191914, 190324, 179406, 204214, 203097, 107992, 208530, 191548, 200894,
           205968, 200785, 190382, 209496, 163811, 187549, 193973, 197520,
            202901, 200065, 191570, 189120, 190011, 187849, 206168, 196215, 193328, 196055,
           200052, 210283, 167403, 203488, 207284, 196049, 201073, 199887, 207360, 191545,
           185264, 202526, 203643, 201680, 191631, 190725, 191920, 193800, 207370, 207364,
           202925, 182019, 200896, 194463, 193966, 207182, 206657, 195691, 201272, 205629,
           194909, 194856, 197071, 201923, 195986, 204768, 196533, 205966, 195694, 200900]

stringMovie = [str(int) for int in movieNums]
user_list = []
score_list = []
id_list = []

# 영화 댓글 크롤링
for each_movieNum in tqdm(range(len(movieNums))):
    url_pre = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + stringMovie[each_movieNum] + '&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='

    for page in range(100):
        # print('\n', page + 1, "페이지\n")
        site = url_pre + str(page + 1)  # 1 ~ 100까지 변환됨. 100*10 = 총 1,000개 댓글 수집
        browser.get(site)
        time.sleep(1)
        page = browser.page_source
        soup = BeautifulSoup(page, "html.parser")  # get HTML text

        scores = soup.find_all('div', 'star_score')
        for score in scores:
            score = score.get_text()
            score = score.strip()
            score_list.append(score)

        movie = soup.select('div.score_reple')
        for userID in movie:
            userIds = userID.select('em a span')
            id_list.append(userIds[0].text)

    for i in range(len(score_list)):
        append_list = [each_movieNum+1, stringMovie[each_movieNum], score_list[i], id_list[i]]
        user_list.append(append_list)

# convert list to dataframe
movie_user_df = pd.DataFrame(user_list, columns=['movieRank', 'movieId', 'score', 'userId'])
save_fname = 'C:\\Users\\komac\\Desktop\\PythonWorkspace\\DSOB\\team\\output\\movie_user.csv'
movie_user_df.to_csv(save_fname, encoding='utf-8-sig')   # save the DataFrame to csv file
