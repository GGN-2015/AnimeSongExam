import os
import random

from DirUtils  import DirUtils
from TxtParser import TxtParser

# 在 bootstrap 里打一个 badge
def green_badge(s: str) -> str:
    if s.strip() == "":
        return ""
    return "<span class=\'badge text-bg-success\'>%s</span>" % s
    #return s

# 获取所有可能成为问题答案的项目
class Answers:
    def __init__(self, dir_utils: DirUtils, txt_parser:TxtParser):
        self.dir_utils   = dir_utils
        self.txt_parser  = txt_parser
        self.last_answer = None
    # 在指定的可行列表中筛选符合年份要求的歌曲
    def select_song_list_by_year(self, allanime, year_from, year_to) -> list:
        song_list  = []
        for filepath in allanime:
            dic, _ = self.txt_parser.parsefile(filepath) # 解析文件
            assert dic.get("name") is not None           # 必须指明名字
            assert dic.get("quarter") is not None        # 必须指明季度
            anime_name = dic["name"]                     # 获取名称
            quarter    = dic.get("quarter")              # 获取年月
            year       = int(quarter.split("-")[0])      # 获取年份
            dirnow     = os.path.dirname(filepath)       # mp3 文件必须存储在 txt 文件同目录下
            if year_from <= year <= year_to:             # 如果在指定年份区间里
                for term in dic:     
                    song_name = dic[term]
                    if term.endswith(".mp3"):
                        tag  = anime_name + " " + green_badge(term[:-4]) + " " + song_name
                        file = os.path.join(dirnow, term)
                        assert os.path.isfile(file)
                        final_file = os.path.relpath(file, self.dir_utils.get_data_dir()).replace("\\", "/")
                        song_list.append({
                            "tag" : tag, # 歌曲的显示名称
                            "file": final_file # 歌曲比较的主键：文件路径
                        })
        return song_list
    # 获取 data 文件夹下的所有动漫音乐
    def get_all_anime_song(self, year_from, year_to) -> list:
        allanime = self.dir_utils.scan_data_dir_with_filename("anime.txt")
        return self.select_song_list_by_year(allanime, year_from, year_to)
    # 获得所有电影中的音乐
    def get_all_movie_song(self, year_from, year_to):
        allanime = self.dir_utils.scan_data_dir_with_filename("movie.txt")
        return self.select_song_list_by_year(allanime, year_from, year_to)
    # 获取所有日文 vocaloid 音乐
    def get_all_jpnv_song(self, year_from, year_to):
        allanime = self.dir_utils.scan_data_dir_with_filename("jpn_vocaloid.txt")
        return self.select_song_list_by_year(allanime, year_from, year_to)
        return []
    # 获取中文 vocaloid 音乐
    def get_all_chnv_song(self, year_from, year_to):
        allanime = self.dir_utils.scan_data_dir_with_filename("chn_vocaloid.txt")
        return self.select_song_list_by_year(allanime, year_from, year_to)
    # 获取所有歌曲
    def get_all_song(self, year_from, year_to, anime: bool, movie: bool, jpnv: bool, chnv: bool):
        arr = []
        if anime:
            arr += self.get_all_anime_song(year_from, year_to)
        if movie:
            arr += self.get_all_movie_song(year_from, year_to)
        if jpnv:
            arr += self.get_all_jpnv_song(year_from, year_to)
        if chnv:
            arr += self.get_all_chnv_song(year_from, year_to)
        return arr
    # 生成一个随机问题
    def generate_random_question(self, options_cnt: int, year_from, year_to, anime: bool, movie: bool, jpnv: bool, chnv: bool):
        assert options_cnt >= 2 # 至少要有两个选项
        all_song = self.get_all_song(year_from, year_to, anime, movie, jpnv, chnv)
        if options_cnt > len(all_song):
            return [] # 返回一个空问题，表示不存在合法的问题
        else:
            ans_list = random.sample(all_song, options_cnt)
            retry_cnt = 0
            while ans_list[0] == self.last_answer and retry_cnt < 3: # 尽可能保证相邻两次查询答案不同
                retry_cnt += 1
                ans_list = random.sample(all_song, options_cnt)
            self.last_answer = ans_list[0] # 更新最后出现的答案
            return ans_list

if __name__ == "__main__":
    dir_utils  = DirUtils()
    txt_parser = TxtParser()
    answers    = Answers(dir_utils, txt_parser)
    for pr in answers.generate_random_question(4, 1908, 2100, True, True, True, True):
        print(pr)