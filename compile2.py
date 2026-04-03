import urllib.request
import urllib.parse
import json

# Read the LaTeX source
with open('cv.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

print("Trying latex.ytotech.com API...")
try:
    payload = json.dumps({
        "compiler": "pdflatex",
        "resources": [{"main": True, "content": tex}]
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://latex.ytotech.com/builds/sync',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as res:
        content = res.read()
        print(f"Response size: {len(content)} bytes")
        print(f"First bytes: {content[:8]}")
        if content[:4] == b'%PDF':
            with open('cv.pdf', 'wb') as f:
                f.write(content)
            print("SUCCESS: cv.pdf written!")
        else:
            print("ERROR: Got non-PDF response:")
            print(content[:500])
except Exception as e:
    print(f"Failed: {e}")
