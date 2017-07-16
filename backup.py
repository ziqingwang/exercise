
# -*- coding: utf-8 -*-

#  srcDir是待备份文件
#  dstDir/md5.data是保存md5值的地方
#  tar = tarfile.open(os.path.join(baseDir,dstDir,fullName),'w:gz')是全局备份文件的地方
#  tar = tarfile.open(os.path.join(baseDir,dstDir,incrName),'w:gz')是增量备份文件的地方


import time
import os 
import cPickle as p 
import tarfile                                              #方便的读取tar归档文件
import hashlib

baseDir = 'C:\Users\lenovo\Desktop'
srcDir = 'a'
dstDir = 'b'
fullName = 'full_%s_%s.tar.gz' % (srcDir,time.strftime('%Y%m%d'))
incrName = 'incr_%s_%s.tar.gz' % (srcDir,time.strftime('%Y%m%d'))
md5file = 'md5.data'

def md5sum(fname):
	m = hashlib.md5()                                       #将data数据转变成一组md5值
	with file(fname) as f:
		while True:
			data = f.read(4096)                            #以4k读取，防止文件过大，内存超载
			if len(data) == 0:
				break
			m.update(data)                               #将后面读入的数据添加到之前，并综合所有数据进行转换md5值

	return m.hexdigest()                               #返回最后的md5值

def fullBackup():                               #进行全局备份
	md5Dict = {}
	fileList = os.listdir(os.path.join(baseDir,srcDir))             #os.listdir(path)返回指定的目录和文件夹
	for eachFile in fileList:
		md5Dict[eachFile] = md5sum(os.path.join(baseDir,srcDir,eachFile))    #以文件名为key，srcDir的md5值为value，创建字典

	with file(os.path.join(baseDir,dstDir,md5file),'w') as f:                   #b/md5.data
		p.dump(md5Dict,f)                  #将md5Dict中的value以特定格式读取到b/md5.data文件中

	tar = tarfile.open(os.path.join(baseDir,dstDir,fullName),'w:gz')   #创建tar压缩包名
	os.chdir(baseDir)                                          #切换路径到baseDir目录
	tar.add(srcDir)
	tar.close()

def incrBackup():                                      #进行增量备份
	newmd5 = {}
	fileList = os.listdir(os.path.join(baseDir,srcDir))
	for eachFile in fileList:
		newmd5[eachFile] = md5sum(os.path.join(baseDir,srcDir,eachFile))
	with file(os.path.join(baseDir,dstDir,md5file)) as f:
		storedmd5 = p.load(f)                            #以原格式输入=出b/md5.data文件中的value

	tar = tarfile.open(os.path.join(baseDir,dstDir,incrName),'w:gz')  #创建压缩包增量
	os.chdir(baseDir)
	for eachKey in newmd5:
		if(eachKey not in storedmd5) or (newmd5[eachKey] != storedmd5[eachKey]):  #判断是否有新的文件和是否原来文件被改变，若改变，则将其添加到tar中
			tar.add(os.path.join(srcDir,eachKey))
	tar.close()

	with file(os.path.join(baseDir,dstDir,md5file),'w') as f:   #将新产生的md5值添加到b/md5.data中
		p.dump(newmd5,f)


def main():
	if time.strftime('%a') == 'Mon':   #每周一进行全局备份，其他时间进行增量备份
		fullBackup()
	else:
		incrBackup()

if __name__ == '__main__':
	main()

