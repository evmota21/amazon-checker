import urllib.request

url = "http://download.thinkbroadband.com/10MB.zip"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 ' \
             'Safari/605.1.15 '

file_name = url.split('/')[-1]
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
u = urllib.request.urlopen(req)
f = open(file_name, 'wb')
meta = u.info()
print(meta)
file_size = int(meta.get_all("Content-Length")[0])
print("Downloading: %s Bytes: %s" % (file_name, file_size))

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8) * (len(status) + 1)
    print(status, )

f.close()
