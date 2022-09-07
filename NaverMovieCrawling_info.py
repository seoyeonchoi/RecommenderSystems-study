from tqdm import tqdm
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# parameters
driver_path = 'C:\\Users\\komac\\Desktop\\PythonWorkspace\\DSOB\\resources\\chromedriver95.exe' # 각자 크롬 드라이버 경로

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

# 영화 정보 크롤링
movie_list = []

for i in tqdm(range(len(movieNums))):
    movie_info_link = 'https://movie.naver.com/movie/bi/mi/basic.naver?code='
    site = movie_info_link + stringMovie[i]  # 1 ~ 10까지 변환됨.
    browser.get(site)
    time.sleep(1)
    page = browser.page_source
    each_info_soup = BeautifulSoup(page, "html.parser")  # get HTML text
    # title
    movie_title = each_info_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')
    movie_title = movie_title.text
    # genre
    movie_genre = each_info_soup.find('dl', {'class':"info_spec"})
    movie_genre = movie_genre.span.text
    movie_genre = movie_genre.replace("\n","")
    movie_genre = movie_genre.replace("\t","")
    movie_genre = movie_genre.replace('"', "")
    # list 합치기
    movie_info_list = [i+1, movieNums[i], movie_title, movie_genre]
    # list append
    movie_list.append(movie_info_list)

# convert list to dataframe
movie_info_df = pd.DataFrame(movie_list, columns=['movieRank', 'movieId', 'score', 'userId'])
save_fname = 'C:\\Users\\komac\\Desktop\\PythonWorkspace\\DSOB\\team\\output\\movie_info.csv'
movie_info_df.to_csv(save_fname, encoding='utf-8-sig')   # save the DataFrame to csv file


