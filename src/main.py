import os
import random
from flask import Flask, render_template, send_file

from DirUtils  import DirUtils
from TxtParser import TxtParser
from Answers   import Answers

dir_utils  = DirUtils()
txt_parser = TxtParser()
answers    = Answers(dir_utils, txt_parser)
app        = Flask(__name__)

# 首页
@app.route('/')
def index():
    options = answers.generate_random_question(4)
    answer  = random.sample(options, 1)[0]
    return render_template('index.html', options=options, answer=answer)

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