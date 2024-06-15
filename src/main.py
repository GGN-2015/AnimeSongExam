import os
import random
from flask import Flask, render_template, send_file, request

from DirUtils  import DirUtils
from TxtParser import TxtParser
from Answers   import Answers

dir_utils  = DirUtils()
txt_parser = TxtParser()
answers    = Answers(dir_utils, txt_parser)
app        = Flask(__name__)

# 如果是合法整数，则返回，否则返回默认值
def wrap_int(x: str, default_v:int):
    try:
        x = int(x)
    except:
        x = default_v
    return x

# 首页
@app.route('/')
def index():
    year_from      = wrap_int(request.args.get("year_from", ""), 1908)
    year_to        = wrap_int(request.args.get("year_to", ""), 2100)
    year_to        = max(year_to, year_from)
    anime_checkbox = request.args.get("anime_checkbox", "0")
    movie_checkbox = request.args.get("movie_checkbox", "0")
    jpn_vocaloid   = request.args.get("jpn_vocaloid_checkbox", "0")
    chn_vocaloid   = request.args.get("chn_vocaloid_checkbox", "0")
    if set([anime_checkbox, movie_checkbox, jpn_vocaloid, chn_vocaloid]) == set(["0"]):
        anime_checkbox = "1"
        movie_checkbox = "1"
        jpn_vocaloid   = "1"
        chn_vocaloid   = "1" # 默认全选
    options = answers.generate_random_question(4, year_from, year_to, anime_checkbox=="1", movie_checkbox=="1", jpn_vocaloid=="1", chn_vocaloid=="1")
    if options != []:
        answer = options[0] # 默认第一个选项是答案
    else:
        answer = None       # 问题不存在
    random.shuffle(options) # 重新打乱
    return render_template('index.html', 
        options=options, 
        answer=answer,
        year_from=year_from,
        year_to=year_to,
        anime_checkbox=anime_checkbox,
        movie_checkbox=movie_checkbox,
        jpn_vocaloid_checkbox=jpn_vocaloid,
        chn_vocaloid_checkbox=chn_vocaloid)

# 提供音频文件的接口
@app.route('/audio/<path:file_path>')
def serve_audio(file_path: str):
    assert file_path.endswith(".mp3")
    data_dir = dir_utils.get_data_dir()
    file     = os.path.join(data_dir, file_path)                 # 获取绝对路径
    assert dir_utils.is_path_in_another(file, data_dir)          # 不允许获取 data 目录外的文件
    return send_file(file, as_attachment=True, conditional=True) # 发送 mp3 文件

if __name__ == '__main__':
    app.run(debug=True)