import os
import sys
import random
import requests
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

if len(sys.argv) < 2:
	sys.exit("Usage: convertStream.py [URL/m3u8 file] [mp4 filename *optional]\nm3u8 file must be m3u8 extention")

path = os.getcwd()
baseurl = sys.argv[1]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
m3u8_file = baseurl
if baseurl.startswith("http"):
	m3u8_file = path+"\\"+id_generator()+".m3u8" # the name you want to save file as
	if ".m3u8" in baseurl:
		filename = baseurl.split("/")[len(baseurl.split("/"))-1].split(".m3u8")[0]
		m3u8_file = path+"\\"+filename+".m3u8"
	print("Converting video from "+baseurl)
	resp = requests.get(baseurl, headers=headers) # making requests to server
	with open(m3u8_file, "wb") as f:
		f.write(resp.content) # writing content to file
else:
	if not os.path.isfile(m3u8_file):
		sys.exit("Usage: convertStream.py [URL/m3u8 file] [mp4 filename *optional]\nm3u8 file must be m3u8 extention")
	elif not m3u8_file.endswith("m3u8"):
		sys.exit("Usage: convertStream.py [URL/m3u8 file] [mp4 filename *optional]\nm3u8 file must be m3u8 extention")
#m3u8_To_MP4.multithread_download('http://videoserver.com/playlist.m3u8')
#m3u8_To_MP4.multithread_file_download('https://hls.vdtuzv.com/videos4/e44faaf9622c783032d64e7c28fbd0a4/e44faaf9622c783032d64e7c28fbd0a4.m3u8?auth_key=1724121678-66c4024e723a2-0-9063fc91f79dabb0d6ae357c5e67f602&v=3&time=0',"test.mp4")

mp4_file = m3u8_file.split(".m3u8")[0]+".mp4"
if len(sys.argv) >= 3:
	mp4_file = sys.argv[2]

os.system("ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "+m3u8_file+" -c copy -bsf:a aac_adtstoasc "+mp4_file)
