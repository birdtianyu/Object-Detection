import re
import urllib.request
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from CallProgressBar import MyProgressBar

# 控制百度图片下载
class DownLoadControl(object):
    def __init__(self, SearchWord, Number, Directory, Label):
        super(DownLoadControl, self).__init__()
        # self.SUM_PAGES = 30             # 下载图片页数
        self.SUM_NUMBER = int(Number)          # 下载图片的数量
        self.KEYWORD = str(SearchWord)         # 要搜索的关键字
        self.DIRECTORY = str(Directory)        # 默认下载文件夹地址
        self.LABEL = str(Label)                # 下载图片的标签

        #!!!这个变量很重要
        self.fanye_count = 0              # 累计翻页数
        self.NumTemp = 0                  # 已经成功下载了几张图片

    def get_OnePage_ImgUrls(self, onepageurl):
        """获取单个翻页的所有图片的urls+当前翻页的下一翻页的url"""
        if not onepageurl:
            print('已到最后一页, 结束')
            return [], ''
        try:
            html = requests.get(onepageurl).text                  # 整个HTML文本
            # print("html Text:\n", html)
        except Exception as e:
            print(e)
            pic_urls = []
            fanye_url = ''
            return pic_urls, fanye_url
        pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)    # 利用正则表达式查找目标文本
        fanye_urls = re.findall(re.compile(u'<a href="(.*)" class="n">'), html)
        # print("fanye_urls: ",fanye_urls)
        # 因为前四页没有返回上一页选项
        if fanye_urls and self.fanye_count <= 3:
            fanye_url = 'http://image.baidu.com' + fanye_urls[0]
        elif fanye_urls and self.fanye_count > 3:
            fanye_url = 'http://image.baidu.com' + fanye_urls[1]   # [上一页, 下一页]
        else:
            fanye_url = ''
        return pic_urls, fanye_url

    def downloadImgs(self, ImgURLs, OutPut):
        """给出图片链接列表, 下载所有图片"""
        num = 0  # 计算已经下载了几张图片
        for i, pic_url in enumerate(ImgURLs):
            if num <= self.SUM_NUMBER:
                try:
                    pic = requests.get(pic_url, timeout=15)   # 最大支持15秒延迟
                    string = self.DIRECTORY + "\\" + self.LABEL + str(num + 1) + '.jpg'
                    with open(string, 'wb') as f:
                        f.write(pic.content)
                        print('成功下载第%s张图片' % str(num + 1))
                        temp1 = '成功下载第%s张图片' % str(num + 1)
                        OutPut.setLabelText(temp1)
                        self.NumTemp = self.NumTemp + 1
                        OutPut.setPercent((self.NumTemp / self.SUM_NUMBER) * 100)
                        QApplication.processEvents()                     # 实时显示
                        num = num + 1
                        while OutPut.getstate() is False:
                            print("******************************************************************")
                            return

                except Exception as e:
                    print('下载列表中第%s个链接图片时失败: %s' % (str(i + 1), str(pic_url)))
                    print('失败原因:', e)                # 打印下载错误原因
                    print('现已自动跳过该链接')
                    temp2 = "下载列表中第%s个链接图片时失败, 已跳过该链接" % (str(i + 1))
                    OutPut.setLabelText(temp2)
                    QApplication.processEvents()
                    continue
            else:
                break

    def Main(self):
        """主执行函数"""
        # 百度图片官网
        BaiduImage_url = r'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497491098685_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1497491098685%5E00_1519X735&word='
        url_init = BaiduImage_url + urllib.request.quote(self.KEYWORD, safe='/')
        all_pic_urls = []

        # 创建一个进度条
        ProgressBarObject = MyProgressBar()
        ProgressBarObject.show()      # 不能callable
        QApplication.processEvents()  # 实时显示

        onepage_urls, fanye_url = self.get_OnePage_ImgUrls(url_init)
        all_pic_urls.extend(onepage_urls)

        while len(list(set(all_pic_urls))) < self.SUM_NUMBER + 20:  # 下载几页, 容错率,允许20个链接出错
            onepage_urls, fanye_url = self.get_OnePage_ImgUrls(fanye_url)
            self.fanye_count += 1
            print('第%s页%s' % (self.fanye_count, fanye_url))
            # strTemp = '第%s页%s' % (self.fanye_count, fanye_url)
            # ProgressBarObject.setLabelText(strTemp)
            # QApplication.processEvents()  # 实时显示
            if fanye_url == '' and onepage_urls == []:
                break
            all_pic_urls.extend(onepage_urls)

        # print("本次共获取到%s个图片的URL" % len(list(set(all_pic_urls))))
        print("***开始执行下载***\n")
        ProgressBarObject.setLabelText("***开始执行下载***")
        QApplication.processEvents()  # 实时显示
        self.downloadImgs(list(set(all_pic_urls)), ProgressBarObject)  # 利用set结构删掉重复的url

    def Test(self):
        """测试用函数"""
        pass




