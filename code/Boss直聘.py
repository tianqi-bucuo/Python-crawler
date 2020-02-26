#encoding: utf-8

# 导入etree时需要手动，不会有提示
from lxml import etree

text = """
<table class="tablelist" cellpadding="0" cellspacing="0">
    <tbody>
        <tr class="h">
            <td class="l" width="374">职位名称</td>
            <td>职位类别</td>
            <td>人数</td>
            <td>地点</td>
            <td>发布时间</td>
        </tr>
        <tr class="even">
            <td class="l square"><a target="_blank" href="position_detail.php?id=33824&amp;keywords=python&amp;tid=87&amp;lid=2218">22989-金融云区块链高级研发工程师（深圳）</a></td>
            <td>技术类</td>
            <td>1</td>
            <td>深圳</td>
            <td>2017-11-25</td>
        </tr>
"""


# 从字符串中读取
def parse_text():
    htmlElement = etree.HTML(text)
    print(etree.tostring(htmlElement,encoding='utf-8').decode("utf-8"))

# 从文件中读取html代码
def parse_tencent_file():
    htmlElement = etree.parse("tencent.html")
    print(etree.tostring(htmlElement, encoding='utf-8').decode('utf-8'))

# 解析html，指定解析器，有时候html代码不规范需要指定解析器
def parse_lagou_file():
    # 指定解析器
    parser = etree.HTMLParser(encoding='utf-8')
    htmlElement = etree.parse("lagou.html",parser=parser)
    print(etree.tostring(htmlElement, encoding='utf-8').decode('utf-8'))



if __name__ == '__main__':
    parse_text()
    # parse_file()
    # parse_lagou_file()