import io
import lxml.etree
import lxml.html


def create_from_string(text, encode='utf-8'):
    source = io.BytesIO(text.encode(encode))

# 迭代读取 HTML 文件
with open('example.html', 'rb') as f:
    context = lxml.etree.iterparse(f, html=True, load_dtd=True)

    # 遍历节点
    for action, elem in context:
        # 如果节点是 title 标记，则输出标题信息
        if elem.tag == 'title':
            print('Title:', elem.text)

        # 如果节点是 a 标记，则输出链接信息
        elif elem.tag == 'a':
            print('Link:', elem.get('href'))

        # 删除解析完毕的节点
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]


# 加载 HTML 文件
doc = lxml.html.parse('example.html').getroot()

# 获取 HTML 标题
title = doc.find('.//title').text

# 获取 HTML 页面的所有链接
links = [a.get('href') for a in doc.cssselect('a')]

# 输出结果
print('Title:', title)
print('Links:', links)
