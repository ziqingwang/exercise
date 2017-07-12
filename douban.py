#coding:utf-8
# 使用xpath,requests抓取豆瓣电影top250信息
import requests
from lxml import html
import sys
reload(sys)
sys.setdefaultencoding("utf8")
k=1
for i in range(10):
	url = "https://movie.douban.com/top250?start={}&filter=".format(i*25)
	con = requests.get(url).content
	sel = html.fromstring(con)
	for i in sel.xpath('//div[@class="info"]'):  #电影的介绍块，内含各种信息
		title = i.xpath ('div[@class="hd"]/a/span[@class="title"]/text()')[0] #取出电影标题
		info = i.xpath('div[@class="bd"]/p/text()') #取出主演，国别等信息
		info_1 = info[0].replace(" ","").replace("\n","") #取出主演 ，导演
		date = info[1].replace(" ","").replace("\n","").split("/")[0] #取出出品日期
		country = info[1].replace(" ","").replace("\n","").split("/")[1] #国别
		geners = info[1].replace(" ","").replace("\n","").split("/")[2] #影片类型
		rate = i.xpath('//span[@class="rating_num"]/text()')[0] #评分
		comCount = i.xpath('//div[@class="star"]/span[4]/text()')[0] #评价人数
		print "top%s" % str(k)
		#print title ,info_1,rate,date,country,geners,comCount
		with open ("top250.txt","a") as f: #将信息保存在文档
			f.write("TOP%s\n影片名称:%s\n评分:%s %s上映日期:%s\n上映国家:%s\n%s\n" %(k,title,rate,comCount,date,country,info_1))
			f.write("..........................\n")
		k += 1