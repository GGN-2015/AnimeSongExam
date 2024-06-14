import os

# 与目录遍历相关的功能
class DirUtils:
    def __init__(self):
        pass
    # 获取本项目的根目录
    def get_root_dir(self) -> str:
        src_dir  = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(src_dir)
        return root_dir
    # 获取项目的数据目录
    def get_data_dir(self) -> str:
        root_dir = self.get_root_dir()
        return os.path.join(root_dir, "data")
    # 获取一个指定绝对路径中的所有非目录文件
    def __scan_dir(self, filepath: str) -> list:
        assert os.path.isabs(filepath)
        if os.path.isfile(filepath): # 返回一个文件的绝对路径
            return [filepath]
        elif os.path.isdir(filepath): # 返回文件夹中的所有文件的绝对路径
            arr = []
            for file in os.listdir(filepath):
                subfilepath = os.path.join(filepath, file)
                arr += self.__scan_dir(subfilepath)
            return arr
        else:
            return []
    # 获取 data 文件中的所有非目录文件
    def scan_data_dir(self) -> list:
        data_dir = self.get_data_dir()
        return self.__scan_dir(data_dir)
    # 获取 data 文件中的所有具有指定名字的非目录文件
    def scan_data_dir_with_filename(self, filename:str) -> list:
        arr = []
        for line in self.scan_data_dir():
            if os.path.basename(line) == filename:
                arr.append(line)
        return arr
    # 判断目录之间的包含关系
    def is_path_in_another(self, sub_path, parent_path) -> bool:
        try:
            common_path = os.path.commonpath([sub_path, parent_path])
            return common_path == parent_path
        except (ValueError, TypeError):
            return False

# 测试
if __name__ == "__main__":
    dirutils = DirUtils()
    print("\n".join(dirutils.scan_data_dir_with_filename("anime.txt")))