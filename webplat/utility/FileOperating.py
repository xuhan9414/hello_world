import os
import time
'''
文件操作类
'''

class FileOperating:
     # 默认存放数据处理csv文件的路径
    def __init__(self, path, user_id):
        self.p = path
        self.u = user_id

    '''
    根目录创建
    '''
    def root_creating(self):
         if os.path.exists(self.p):
             print('根目录' + self.p + '已经存在！')
         else:
             os.makedirs(self.p)
             print('根目录' + self.p + '创建完成！')

    '''
     创建文件目录
     self：默认路径
     user_id：用户名
    '''

    def file_creating(self):
         date = time.strftime('%Y-%m-%d', time.localtime(time.time())) #获取日期
         clock = time.strftime('%H-%M-00', time.localtime(time.time())) #获取时间
         final_path = self.p + '/' + self.u +'/' + date + '/' + clock

         if os.path.exists(self.p):
            if os.path.exists(final_path):
                print('该目录已存在')
            else:
                # 若不存在，直接创建多级目录（用户名-操作日期-操作时间）
                os.makedirs(final_path)
                print('创建目录' + final_path +'完成')
            return final_path, date, clock

         else:
             print('请输入正确的保持地址!')
             return  '请输入正确的保持地址! '

         '''
         查询文件夹中所有下一级的文件夹/文件
         输入：file_path, 格式 C..\\..\\..
         返回：file_1st:[所有文件名称]
         '''

    def file_searching(self):
        file_1st = []
        for filename in os.listdir(self.p):
            file_1st.append(filename)
        return file_1st

    '''
     查询一个用户下所有文件夹
     查询分两级
    '''
    def user_searching(self):
        lst = []
        for dl in os.listdir(self.p):
            f = self.p + '\\' +dl
            for tl in os.listdir(f):
                if os.listdir(f + '\\' + tl):
                    lst.append(dl + ',' + tl)

        return lst