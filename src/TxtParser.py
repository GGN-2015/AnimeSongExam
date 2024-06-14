# 用于解析文本文件
class TxtParser:
    def __init__(self):
        pass
    def parsefile(self, filepath: str): # 解析文本文件
        fp      = open(filepath, "r", encoding="utf-8")
        content = fp.read().split("\n")
        dic = {} # 用于记录字典数据
        lst = [] # 用于记录非字典数据
        for line in content:
            line = line.strip()              # 忽略行首和行末的空白字符
            if line == "" or line[0] == "#": # 跳过注释内容以及空行
                continue
            if line.find(";") != -1: # 字典数据
                keyname, value = line.split(";", maxsplit=1)
                dic[keyname] = value
            else:                    # 列表数据（非字典数据）
                lst.append(line)
        return dic, lst

if __name__ == "__main__":
    from Dirutils import Dirutils
    dirutils = Dirutils()
    testfile = dirutils.scan_data_dir_with_filename("anime.txt")[1]
    parser   = TxtParser()
    print(parser.parsefile(testfile))