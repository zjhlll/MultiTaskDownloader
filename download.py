# coding:utf-8

"""使用多任务完成对单个文件的下载，提高下载的速度"""
import os
import sys
import gevent
from gevent import monkey  # 使用协程一定记得打包

monkey.patch_all()

def main():
    # 使用sys模块可以提高代码的通用性，方便在命令行执行时，指定下载的参数
    # filename = sys.argv[1]
    filename = "test.png"
    # 假定下载的资源都存在当前目录下的mode文件夹内
    src = "./mode/"
    # 判断文件是否存在
    if filename in os.listdir("./mode/"):
        # 拼接路径
        filepath = src + filename
        # new_name = sys.argv[2]
        new_name = filename
        # 先创建一个文件，
        with open(new_name,"wb") as f:
            pass
        # with open(filepath,"rb") as r:
        #     content = r.read()
        #     with open(new_name,"wb") as w:
        #         w.write(content)
        # 判断文件的大小
        size = os.path.getsize(filepath)
        # 分成三分的话 对三求余 对三取整
        part = 3
        # 前三分的大小为 size//3  后一份的大小为 size%3
        part_size = size//part
        # 定义一个列表，存放所有的协程
        ge_list = list()
        for i in range(4):
            ge = gevent.spawn(read_write,*(filepath,new_name,i*part_size,part_size))
            ge_list.append(ge)
        gevent.joinall(ge_list)
    else:
    	print("资源不存在")
def read_write(filename,new_name,start,size):
	"""filename为源文件，new_name为新文件，start表示读取的开始，size表示读取的大小"""
    print("协程开始")
    with open(filename,"rb") as r:
    	# 定位文件的指针
        r.seek(start,0)
        content = r.read(size)
        with open(new_name,"rb+") as w:
            w.seek(start,0)
            w.write(content)



if __name__ == "__main__":
    main()
