import urllib.request, urllib.parse, sys
try:
    with open('cv.tex', 'r', encoding='utf-8') as f:
        text = f.read()
    url = 'https://latex.vercel.app/compile'
    data = urllib.parse.urlencode({'text': text}).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as response:
        with open('cv.pdf', 'wb') as out_f:
            out_f.write(response.read())
    print("Compiled successfully!")
except Exception as e:
    print("Failed: ", e)
