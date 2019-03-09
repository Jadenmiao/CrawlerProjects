import wx   # 导入wx模块，做GUI窗口
import os   # 系统模块

'''
    根据线路文件生成路程键值对格式
'''
Line_Info = {}   # 空字典，存储站点信息
filePath = r'.\线路图'                # 只读方式打开文件夹
files = os.listdir(filePath)        # 获取指定文件夹中所有内容的名称列表
files = [os.path.join(filePath, file) for file in files]  # 路径名连接成字符串
# print(files)   files为一个列表，元素为str格式的路径： '.\\线路\\一号线.txt'
for file in files:
    with open(file, 'rb') as f:  # 以二进制形式打开文件用于只读，默认文件打开方法
        for line in f:
            line = line.decode('utf8')  # 编码选utf8，转换成中文格式
            line_start, line_end = line.split('\t')[0].split('——')  # 起点——终点
            # 上一行注释：split()函数 通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则仅分隔 num 个子字符串
            # 站点为键，然后又是一个字典，里面是终点还有距离，此为一个键值
            distance = line.split('\t')[1]  # 距离则采用一个分隔符，同上，是水平制表(\t)。
            try:
                if Line_Info[line_start]:
                    Line_Info[line_start].update({line_end : int(distance)})  # update函数，更新键值，即更新站点数据
            except:
                    Line_Info[line_start] = {line_end : int(distance)}
            try:
                if Line_Info[line_end]:

                    Line_Info[line_end].update({line_start : int(distance)})
            except:
                    Line_Info[line_end] = {line_start : int(distance)}
            #  防止异常，将线路图最终转化成键值对
# print(Line_Info)  # (调试用) '苹果园':{'古城':2606}

# Dijkstra算法：
# 每次找到离所设置起点最近的一个顶点，然后以该顶点为中心进行向外扩展
# 最终找到的即为起点到其余所有点的最短路径


def dijkstra(line_Info, StartPoint, INF=float('inf')):
    """
        使用 Dijkstra 算法计算指定起始点 startPoint 到图 line_Info 中任意点的最短路径的距离
        INF 为设定的无限远距离值
        无向图 G<V, E>
    """
    book = set()  # 定义一个空集合
    min_V = StartPoint  # 起点设置

    # 起点到其余各顶点的初始路程， 除源点到源点以外都设置为INF,即无穷大
    min_E = dict((k, INF) for k in line_Info.keys())  # 初始化，键值（即距离）设置为无穷大
    min_E[StartPoint] = 0   # 相同点则设置为0
    while len(book) < len(line_Info):
        book.add(min_V)  # 确定输入起点的距离（向book集合中加入新元素min_V）
        # print(book) （调试用）
        for w in line_Info[min_V]:  # 以当前点为中心向外扩散
            if min_E[min_V] + line_Info[min_V][w] < min_E[w]:  # 如果从当前点扩展到某一点的距离比已知最短距离小
                min_E[w] = min_E[min_V] + line_Info[min_V][w]  # 对已知距离进行更新

        new = INF
        # 从剩下的未确定点中选择最小距离点作为新的扩散点
        for v in min_E.keys():
            if v in book:
                continue   # 在集合中的就不用查询了
            if min_E[v] < new:
                new = min_E[v]
                min_V = v
    return min_E           # 返回值为最小距离


class MyFrame(wx.Frame):
    """
        计算器界面，用于输入起始点和终点, 确定即可以出结果
    """
    def __init__(self, title):
        self.checkList = []
        wx.Frame.__init__(self, None, -1, title, size=(700, 200))
        self.panel = wx.Panel(self)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)  # 字体设置 （字号，样式，是否倾斜，是否粗体）

        '''起点输入框'''
        # 设置静态文本 ‘起点：’
        startStatic = wx.StaticText(self.panel, -1, '起点:', style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_MIDDLE)
        # 设置起点输入框
        self.startPoint = wx.TextCtrl(self.panel, size=(150, 30), style=wx.TE_MULTILINE)
        # 设置静态文本 ‘起点：’字体大小、型号
        startStatic.SetFont(font)
        # 清除输入文本框按钮，按按钮清除则可以一次性清除
        button1 = wx.Button(self.panel, -1, '清除', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.startButton, button1)
        # 将上面的起点、输入文本框、按钮放在一个Box里面来进行横向排版
        dirSizer1 = wx.BoxSizer()
        dirSizer1.Add(startStatic)
        dirSizer1.Add(self.startPoint)
        dirSizer1.Add(button1, proportion=0)

        '''终点输入框'''
        endStatic = wx.StaticText(self.panel, -1, '终点:', style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_MIDDLE)
        self.endPoint = wx.TextCtrl(self.panel, size=(150, 30), style=wx.TE_MULTILINE)
        endStatic.SetFont(font)
        button2= wx.Button(self.panel, -1, '清除', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.endButton, button2)
        dirSizer2 = wx.BoxSizer()
        dirSizer2.Add(endStatic)
        dirSizer2.Add(self.endPoint)
        dirSizer2.Add(button2, proportion=0)

        '''票价输出框'''
        self.rmb = wx.TextCtrl(self.panel, size=(100, 30), style=wx.CB_READONLY)
        # rmbStatic = wx.StaticText(self.panel, -1, '元', style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_MIDDLE)
        # rmbStatic.SetFont(font)
        button3 = wx.Button(self.panel, -1, '计算票价', size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.outButton, button3)
        dirSizer3 = wx.BoxSizer()
        dirSizer3.Add(self.rmb)
        # dirSizer3.Add(rmbStatic)
        dirSizer3.Add(button3)

        '''界面竖向排列下去'''
        mainSizer1 = wx.BoxSizer(wx.VERTICAL)                       # 竖向排列容器
        mainSizer1.Add(dirSizer1, proportion=-1, flag = wx.CENTER)  # 起点
        mainSizer1.Add(dirSizer2, proportion=-1, flag=wx.CENTER)    # 终点
        mainSizer1.Add(dirSizer3, proportion=-1, flag=wx.CENTER)    # 票价
        # mainSizer1.Add(button3, proportion=-1, flag=wx.CENTER)
        self.panel.SetSizer(mainSizer1)
        self.Center()
        self.Show()

    def startButton(self, event):     # 清除
        self.startPoint.Clear()

    def endButton(self, event):       # 清除
        self.endPoint.Clear()

    def outButton(self, event):       # 计算票价
        '''确定按钮获取路径计算票价'''
        self.rmb.Clear()
        try:
            # 调用Dijkstra函数
            disAll = dijkstra(Line_Info, StartPoint=self.startPoint.GetValue())
            print('成功调用Dijkstra函数')
            # print(disAll)
        except:
            self.rmb.AppendText('没有该起点，请重新确认')
            return None
        try:
            distance = disAll[self.endPoint.GetValue()]
        except:
            self.rmb.AppendText('没有该终点，请重新确认')
            return None

        '''根据计费标准计算计费'''
        if distance / 1000 < 6:
            needRmd = 3
        elif 6 < distance / 1000 < 12:
            needRmd = 4
        elif 12 < distance / 1000 < 22:
            needRmd = 5
        elif 22 < distance / 1000 < 32:
            needRmd = 6
        if distance / 1000 > 32:
            needRmd = 7 + (distance / 1000 - 32) // 20
        self.rmb.AppendText(str(needRmd) + '元 ')   # 距离为' + str(distance) + '米')


if __name__ == '__main__':    # 输出
    app = wx.App()
    MyFrame('北京地铁计算器')
    app.MainLoop()
