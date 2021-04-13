# 数据存储器内容基本不变，只不过生成的文件按照当前时间命名，以避免重复，同时对文件进行缓存写入
import codecs
import time
class DataOutput(object):
    def __init__(self):
        self.filepath = 'baike_%s.html' % time.strftime("%y_%m_%d_%H_%M_%S", time.localtime())
        self.output_head()
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        # 缓存写入，缓存10个再写
        if len(self.datas) > 10:
            self.output_html()

    def output_head(self):
        '''
        将html头写进去
        :return:
        '''
        fout = codecs.open(self.filepath, 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write("<head><meta charset='utf-8'/></head>")  # 解决bug：utf-8后边少了一个'号
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_html(self):
        '''
        写入数据
        :return:
        '''
        fout = codecs.open(self.filepath, 'a', encoding='utf-8')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data.get('url'))
            fout.write('<td>%s</td>' % data.get('title'))
            fout.write('<td>%s</td>' % data.get('summary'))
            fout.write('</tr>')
            self.datas.remove(data)
        fout.close()

    def output_end(self):
        fout = codecs.open(self.filepath, 'a', encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
