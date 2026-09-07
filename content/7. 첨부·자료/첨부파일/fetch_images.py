import urllib.request
import json
import os

os.makedirs(r"C:\Simbio\7. 첨부·자료\첨부파일", exist_ok=True)
headers = {'User-Agent': 'SimbioKnowledgeBot/1.0 (contact: cmksc@naver.com)'}

# 1. Chemical Structure from PubChem REST API
path1 = r"C:\Simbio\7. 첨부·자료\첨부파일\아세트아미노펜_화학구조.png"
pubchem_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/acetaminophen/PNG?image_size=large"
req1 = urllib.request.Request(pubchem_url, headers=headers)
with urllib.request.urlopen(req1) as resp, open(path1, 'wb') as f:
    f.write(resp.read())
print("Pubchem structure:", os.path.exists(path1), os.path.getsize(path1))

# 2 & 3: Query Wikipedia API for direct image URLs
def download_wiki_file(filename, out_path):
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    pages = data['query']['pages']
    for p in pages.values():
        if 'imageinfo' in p:
            direct_url = p['imageinfo'][0]['url']
            print("Direct url:", direct_url)
            req_img = urllib.request.Request(direct_url, headers=headers)
            with urllib.request.urlopen(req_img) as img_resp, open(out_path, 'wb') as out_f:
                out_f.write(img_resp.read())
            print(f"Downloaded {filename} -> {out_path} ({os.path.getsize(out_path)} bytes)")
            return True
    return False

# Download Tylenol bottle and Paracetamol tablets
download_wiki_file("Tylenol Extra Strength.jpg", r"C:\Simbio\7. 첨부·자료\첨부파일\타이레놀_패키지_약통.jpg")
download_wiki_file("Paracetamol tablets.jpg", r"C:\Simbio\7. 첨부·자료\첨부파일\아세트아미노펜_정제_알약.jpg")
