import io
import unittest
from main import ConsoleWriter, ConsoleCounterListener
from html_parser import parse
from lxml import etree

HTML_TEXT = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"></meta>
<title>调用树</title>
<style>body, td, th, p, ul, ol, div {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 10pt;}</style></head>
<body>
<h2>调用树</h2>
<table border="0">
<tr><td><b>Session:</b></td> <td>dsop_core37</td></tr>
<tr><td><b>Time of export:</b></td> <td>2023年4月27日星期四 中国标准时间 下午4:20:27</td></tr>
<tr><td><b>JVM time:</b></td> <td>12:09</td></tr>
<tr><td> </td><td> </td></tr>
<td><b>线程选择: </b></td> <td>所有线程组</td></tr>
<td><b>线程状态: </b></td> <td><img style="vertical-align: middle" "height="6" width="16" border="0" hspace="0" vspace="0" src="jprofiler_images/ff00c400_bff000000.png" /> 就绪(Runnable)</td></tr>
<td><b>聚合级别: </b></td> <td>方法</td></tr>
</table>
<p>aaa</p>

<hr size="1"/><br />
<style>th {border:1px solid #BBBBBB;padding: 3px; margin-bottom: 3px}
td {whitespace:nowrap; padding: 0 3px}</style><table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_tee_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="19" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 39.<wbr />7% - 1,624,655 ms org.<wbr />apache.<wbr />mina.<wbr />filter.<wbr />executor.<wbr />OrderedThreadPoolExecutor$<wbr />Worker.<wbr />run<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_tee_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="19" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 39.<wbr />5% - 1,618,659 ms org.<wbr />apache.<wbr />mina.<wbr />filter.<wbr />executor.<wbr />OrderedThreadPoolExecutor$<wbr />Worker.<wbr />runTasks<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_tee_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="19" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 39.<wbr />5% - 1,618,637 ms org.<wbr />apache.<wbr />mina.<wbr />filter.<wbr />executor.<wbr />OrderedThreadPoolExecutor$<wbr />Worker.<wbr />runTask<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_corner_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="19" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 39.<wbr />5% - 1,618,637 ms org.<wbr />apache.<wbr />mina.<wbr />core.<wbr />session.<wbr />IoEvent.<wbr />run<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_corner_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="19" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 39.<wbr />5% - 1,618,637 ms org.<wbr />apache.<wbr />mina.<wbr />core.<wbr />filterchain.<wbr />IoFilterEvent.<wbr />fire<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_tee_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="18" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 37.<wbr />8% - 1,546,888 ms org.<wbr />apache.<wbr />mina.<wbr />core.<wbr />filterchain.<wbr />DefaultIoFilterChain$<wbr />EntryImpl$<wbr />1.<wbr />messageReceived<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_corner_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="18" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 37.<wbr />8% - 1,546,888 ms org.<wbr />apache.<wbr />mina.<wbr />core.<wbr />filterchain.<wbr />DefaultIoFilterChain.<wbr />callNextMessageReceived<br />
</td>
</tr>
<tr valign="top">
<td nowrap="nowrap"><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_bar_18.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/pixel_transparent_1.gif" /><img height="18" width="18" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/tree/menu_tee_minus_18.gif" /><img height="16" width="16" border="0" align="left" hspace="0" vspace="0" src="jprofiler_images/call_method_16.png" /> <img height="7" width="18" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ff990000.png" /><img height="7" width="0" border="0" hspace="0" vspace="2" src="jprofiler_images/pixel_ffff3300.png" /> 37.<wbr />7% - 1,546,014 ms org.<wbr />apache.<wbr />mina.<wbr />core.<wbr />filterchain.<wbr />DefaultIoFilterChain$<wbr />TailFilter.<wbr />messageReceived<br />
</td>
</tr>
</table></body>
</html>
"""


class TestingCase(unittest.TestCase):

    def test_simple_iterate(self):
        source = etree.fromstring(HTML_TEXT)
        context = etree.iterparse(source)
        for action, elem in context:
            if elem.tag == 'p':
                print(elem.text)

            # 清除处理过的节点
            elem.clear()

            # 遍历该节点之前的兄弟节点，并删除
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    def test_string_input(self):
        source_file = io.BytesIO(HTML_TEXT.encode('utf-8'))
        console_writer = ConsoleWriter()
        console_counter_listener = ConsoleCounterListener()
        parse(source_file, console_writer.listen, 3, ConsoleCounterListener().listen)
        self.assertEqual(8, console_writer.count)
        self.assertEqual(2, console_counter_listener.events)