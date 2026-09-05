---
name: book-digitization
description: Digitize medical textbooks from PDF into high-density Obsidian markdown notes with tightly cropped illustrations, full muscle wikilinking, and zero local bloat.
---

# 📖 Book Digitization & Medical Note Skill (Simbio Standard)

이 스킬은 `G:\내 드라이브\자료 모음\책\` 내의 161권 전문 의학/한의학 교과서 PDF를 읽어 옵시디언 마스터 노트로 변환할 때 사용하는 표준 작업 절차입니다.

---

## 🎯 핵심 불변 규칙 (Core Directives)

1. **분량 및 밀도 (Depth & Volume)**:
   * 한 번에 **60~100페이지 단위**로 분할하여 진행.
   * 요약이나 축약으로 디테일을 날리지 않고, 교과서 원문의 세부 해부학, 생체역학, 임상 테크닉, 증례를 매우 풍부하게 수록.
2. **근육명 및 기존 파일명 100% 위키링크화**:
   * 본문, 목록, 표(Table) 안의 모든 근육 이름([[외복사근]], [[내복사근]], [[외늑간근]], [[장비골근]], [[비복근]] 등)은 **무조건 [[근육명]]**으로 감싼다.
   * 볼트 내에 존재하는 단어(질환, 본초, 처방, 신경, 인대 등)는 웬만하면 [[단어]]로 링크화.
   * **볼드(`**`)와 위키링크는 절대 겹치지 않고 순수 [[근육명]]만 단독 사용**.
3. **혈자리명 표기**:
   * 침구 혈자리(예: `족삼리(足三里)`, `태충(太衝)`)는 [[ ]] 없이 **순수 평문**으로 표기.
4. **도해 정밀 분할 크롭(Tight-crop)**:
   * 페이지 전체 스캔본을 넣지 않고, 각 그림/사진(Fig X.X) 파트와 노란 캡션만 픽셀 단위로 잘라내어 `c:\Simbio\7. 첨부·자료\첨부파일\AnatomyTrains_Fig_*.png`로 저장.
   * **단독 블록 이미지 삽입 (표 내부 삽입 금지)**:
  * 마크다운 표 안에 이미지를 넣으면 파이프(`|`) 파싱 충돌로 렌더링이 깨지므로, **표를 쓰지 않고 단독 블록(단락)**으로 `![[이미지명.png|너비]] 형태로 배치합니다.
5. **로컬 용량 0 byte 원칙**:
   * 원본 PDF는 구글 드라이브 가상 드라이브에서 직접 읽고, 로컬 볼트에는 마크다운 파일과 고순도 크롭 이미지 파일만 저장.

---

## 4. 2개 단위 필수 무결성 검토 (2-Unit Review Checkpoint)
* **2개 분량/챕터 생성 완료 시마다 즉시 1회 전수 검토 수행**:
  1. **이미지 무결성**: 글자 단락이나 페이지 타이틀이 들어가지 않고 **순수 해부학 그림/일러스트/사진만 정밀 추출**되었는지 확인.
  2. **위키링크 무결성**: 모든 근육명([[외복사근]], [[내복사근]], [[비복근]], [[햄스트링]] 등)과 볼트 내 파일명 단어들이 빠짐없이 **순수 [[...]]**로 감싸졌는지 확인.
  3. **서식 무결성**: 깨진 볼드(`**[[...]]**`)나 볼드 파싱 오류가 없는지 확인 후 사용자에게 검토 보고.

## 5. 도해 크롭 파이썬 표준 스니펫

```python
import pymupdf, os, re
from PIL import Image, ImageChops

def extract_tight_figures(pdf_path, out_dir, start_page, end_page):
    doc = pymupdf.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    mat = pymupdf.Matrix(2.0, 2.0)
    fig_pattern = re.compile(r'그림\s*(\d+[\.\_]\d+)', re.IGNORECASE)
    
    for pno in range(start_page, end_page):
        page = doc[pno]
        blocks = page.get_text('blocks')
        page_figs = []
        for b in blocks:
            txt = b[4].strip()
            m = fig_pattern.search(txt)
            if m:
                page_figs.append((m.group(1).replace('_', '.'), pymupdf.Rect(b[:4]), txt))
        if not page_figs:
            continue
        page_figs.sort(key=lambda x: x[1].y0)
        pw, ph = page.rect.width, page.rect.height
        
        for idx, (fnum, cap_rect, cap_txt) in enumerate(page_figs):
            prev_y = page_figs[idx-1][1].y1 if idx > 0 else 30
            top = max(prev_y, cap_rect.y0 - 280)
            bottom = min(ph - 20, cap_rect.y1 + 45)
            left = 30 if cap_rect.x0 < pw * 0.45 else pw * 0.45
            right = pw * 0.55 if cap_rect.x0 < pw * 0.45 and cap_rect.x1 < pw * 0.65 else pw - 30
            clip_rect = pymupdf.Rect(left, top, right, bottom)
            pix = page.get_pixmap(matrix=mat, clip=clip_rect)
            im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            
            # Trim background
            bg = Image.new(im.mode, im.size, (255, 255, 255))
            diff = ImageChops.difference(im, bg)
            diff = ImageChops.add(diff, diff, 2.0, -10)
            bbox = diff.getbbox()
            if bbox:
                im = im.crop(bbox)
            fname = f"AnatomyTrains_Fig_{fnum.replace('.', '_')}.png"
            im.save(os.path.join(out_dir, fname))
```
