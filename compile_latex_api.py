import urllib.request, uuid

def post_multipart(url, fields, files):
    boundary = uuid.uuid4().hex
    headers = {'Content-type': f'multipart/form-data; boundary={boundary}'}
    data = []
    for k, v in fields.items():
        data.extend([
            f'--{boundary}'.encode(),
            f'Content-Disposition: form-data; name="{k}"'.encode(),
            b'',
            v.encode()
        ])
    for k, (filename, content) in files.items():
        data.extend([
            f'--{boundary}'.encode(),
            f'Content-Disposition: form-data; name="{k}"; filename="{filename}"'.encode(),
            b'Content-Type: application/octet-stream',
            b'',
            content
        ])
    data.extend([f'--{boundary}--'.encode(), b''])
    body = b'\r\n'.join(data)
    req = urllib.request.Request(url, data=body, headers=headers)
    return urllib.request.urlopen(req)

try:
    with open('cv.tex', 'rb') as f:
        tex_data = f.read()

    print("Compiling via texlive.net API...")
    res = post_multipart(
        'https://texlive.net/cgi-bin/latexcgi',
        {'filename': 'cv.tex', 'engine': 'pdflatex', 'return': 'pdf'},
        {'filecontents[]': ('cv.tex', tex_data)}
    )
    with open('cv.pdf', 'wb') as f:
        f.write(res.read())
    print("Downloaded successfully as cv.pdf")
except Exception as e:
    print(f"Error: {e}")
