# 数据存储器主要包括两个方法，store_data(data)用于将解析出来的数据存储到内存中
# output_html()用于将存储的数据输出为指定的的文件格式, 此处使用的是将数据存储为HTML格式
import codecs


class DataOutput(object):
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        '''
        暂时存入内存，即datas中
        :param data:
        :return:
        '''
        if data is None:
            return
        self.datas.append(data)

    def output_html(self, filename):
        '''
        将datas中的数据存储到文件中
        :param filename:
        :return:
        '''
        fout = codecs.open(filename, 'w', encoding='utf-8') # codecs处理编码格式
        fout.write('<html>')
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()

