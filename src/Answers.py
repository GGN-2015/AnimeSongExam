import os
import random

from DirUtils  import DirUtils
from TxtParser import TxtParser

# 获取所有可能成为问题答案的项目
class Answers:
    def __init__(self, dir_utils: DirUtils, txt_parser:TxtParser):
        self.dir_utils      = dir_utils
        self.txt_parser     = txt_parser
        self.cached_anwsers = [] # 缓存所有可能答案
    # 获取 data 文件夹下的所有动漫音乐
    def get_all_anime_song(self) -> list:
        if self.cached_anwsers == []:
            allanime = self.dir_utils.scan_data_dir_with_filename("anime.txt")
            song_list  = []
            for filepath in allanime:
                dic, _ = self.txt_parser.parsefile(filepath) # 解析番剧文件
                assert dic.get("name") is not None           # 番剧必须指明名字
                assert dic.get("quarter") is not None        # 番剧必须指明季度
                anime_name = dic["name"]                     # 获取番剧名称
                dirnow     = os.path.dirname(filepath)       # mp3 文件必须存储在 txt 文件同目录下
                for term in dic:     
                    song_name = dic[term]
                    if term.endswith(".mp3"):
                        tag  = anime_name + " " + term[:-4] + " " + song_name
                        file = os.path.join(dirnow, term)
                        assert os.path.isfile(file)
                        final_file = os.path.relpath(file, self.dir_utils.get_data_dir()).replace("\\", "/")
                        song_list.append({
                            "tag" : tag, # 歌曲的显示名称
                            "file": final_file # 歌曲比较的主键：文件路径
                        })
            self.cached_anwsers = song_list
        return self.cached_anwsers
    # 生成一个随机问题
    def generate_random_question(self, answer_cnt: int):
        answer_cnt = min(answer_cnt, len(self.get_all_anime_song()))
        return random.sample(self.get_all_anime_song(), answer_cnt)

if __name__ == "__main__":
    dir_utils  = DirUtils()
    txt_parser = TxtParser()
    answers    = Answers(dir_utils, txt_parser)
    for pr in answers.generate_random_question(4):
        print(pr)