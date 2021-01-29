import sys
import os.path
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from fangPro.spiders.MyDb import MyDb

result=[]
dArray=[]
dArrayJs=[]
class CPdf2TxtManager():
  def __init__(self):
    '''''
    Constructor
    '''
  def changePdfToText(self, path):
    pat = path
    file = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(file)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
      raise PDFTextExtractionNotAllowed
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pdfStr = ''
    # 循环遍历列表，每次处理一个page的内容
    for page in doc.get_pages(): # doc.get_pages() 获取page列表
      interpreter.process_page(page)
      # 接受该页面的LTPage对象
      layout = device.get_result()
      for x in layout:
        if hasattr(x, "get_text"):
          result.append(x.get_text().strip())
          results = x.get_text().strip()
    if os.path.exists(path):  # 如果文件存在
      # 删除文件，可使用以下两种方法。
      os.remove(path)
    for r in result:
      if str(r).find("RW")>=0 or str(r).find("CXJ")>=0 or str(r).find("XH")>=0:
        dArrayJs = dArray
        dArrayJs.pop()
        dArrayJs.pop()
        print(dArrayJs)
        print(len(dArrayJs))
        # 入库
        test = MyDb('localhost', 'root', 'root', 'fang_data')
        print(len(dArrayJs))
        if len(dArrayJs) == 2:
          sql = "insert into yxdj(gfdjh) values (%s);"
          test.insertInfo(sql, (dArrayJs[1]))
        if len(dArrayJs) == 3:
          sql = "insert into yxdj(gfdjh,name) values (%s,%s);"
          test.insertInfo(sql, (dArrayJs[1], dArrayJs[2]))
        if len(dArrayJs) == 44:
          sql = "insert into yxdj(gfdjh,name,card_num) values (%s,%s,%s);"
          test.insertInfo(sql, (dArrayJs[1], dArrayJs[2], dArrayJs[3]))
        if len(dArrayJs) == 5:
          sql = "insert into yxdj(gfdjh,name,card_num,jt_type) values (%s,%s,%s,%s);"
          test.insertInfo(sql, (dArrayJs[1], dArrayJs[2], dArrayJs[3], dArrayJs[4]))
        if len(dArrayJs) == 6:
          sql = "insert into yxdj(gfdjh,name,card_num,jt_type,cdbh) values (%s,%s,%s,%s,%s);"
          test.insertInfo(sql, (dArrayJs[1], dArrayJs[2], dArrayJs[3], dArrayJs[4], dArrayJs[5]))
        if len(dArrayJs) == 7:
          sql = "insert into yxdj(gfdjh,name,card_num,jt_type,cdbh,qt_name) values (%s,%s,%s,%s,%s,%s));"
          test.insertInfo(sql, (dArrayJs[1], dArrayJs[2], dArrayJs[3], dArrayJs[4], dArrayJs[5], dArrayJs[6]))
        if len(dArrayJs) == 8:
          sql = "insert into yxdj(gfdjh,name,card_num,jt_type,cdbh,qt_name,qt_card_num) values (%s,%s,%s,%s,%s,%s,%s));"
          test.insertInfo(sql,
                          (dArrayJs[1], dArrayJs[2], dArrayJs[3], dArrayJs[4], dArrayJs[5], dArrayJs[6], dArrayJs[7]))
        test.close()
        resultYRW = dArray[len(dArray)-1]
        resultINDEX = dArray[len(dArray) - 2]
        dArray.clear()
        dArray.append(resultINDEX)
        dArray.append(resultYRW)



