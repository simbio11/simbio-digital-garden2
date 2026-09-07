import urllib.request
import urllib.parse
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'SimbioKnowledgeBot/1.0 (contact: cmksc@naver.com)'}

def search_wikimedia(query):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&format=json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    results = [item['title'] for item in data['query']['search']]
    return results

def download_file_by_title(title, out_path):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    pages = data['query']['pages']
    for p in pages.values():
        if 'imageinfo' in p:
            direct_url = p['imageinfo'][0]['url']
            print("Downloading from:", direct_url)
            req2 = urllib.request.Request(direct_url, headers=headers)
            with urllib.request.urlopen(req2) as img_resp, open(out_path, 'wb') as out_f:
                out_f.write(img_resp.read())
            print(f"Saved to {out_path} ({os.path.getsize(out_path)} bytes)")
            return True
    return False

# 1. Chemical Structure from Wikimedia
res3 = search_wikimedia("Paracetamol-skeletal.svg")
if res3:
    download_file_by_title(res3[0], r"C:\Simbio\7. 첨부·자료\첨부파일\아세트아미노펜_화학구조.png")

# 2. Paracetamol blister / tablets
res2 = search_wikimedia("Paracetamol 500mg tablets")
if res2:
    download_file_by_title(res2[0], r"C:\Simbio\7. 첨부·자료\첨부파일\아세트아미노펜_정제_알약.jpg")

print("All downloads finished!")
