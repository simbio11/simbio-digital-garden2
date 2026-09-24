---
aliases:
  - cGMP
  - Cyclic GMP
  - Cyclic Guanosine Monophosphate
  - 환상구아노신일인산
tags:
  - 약리
  - 약리성분/세포생물학
  - 혈관이완
title: cGMP
date: 2026-09-13
출처: "PMID: 20606131"
---

# cGMP (Cyclic Guanosine Monophosphate)

> **핵심 요약 (Key Summary)**:
> 산화질소(NO) 및 나트륨이뇨펩타이드 자극에 의해 생성되어 혈관 평활근 이완과 세포 기능을 매개하는 핵심 2차 전달자.
> 구아닐릴 시클라아제(sGC/pGC)에 의해 GTP로부터 합성되고 단백질 인산화효소 G(PKG)를 활성화하여 세포 내 칼슘 감소 유도.
> 한약재 활혈거어약의 eNOS 촉진 하류 혈관 확장 기전 및 PDE5 억제제(실데나필)의 발기부전·폐동맥고혈압 치료 표적.

---

## 1. 기본 화학 정보 & 분자 구조식 (Chemical Identity)

> [!abstract]+ 🧪 3D 약리 분자 구조 (Interactive 3D Viewer)
> <iframe src="https://molecule-viewer-rho.vercel.app/?cid=2405" style="width: 100%; height: 600px; border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);" allowfullscreen></iframe>

| 항목 | 내용 |
| :--- | :--- |
| **물질명** | cGMP (Cyclic Guanosine Monophosphate, 환상 구아노신 일인산) |
| **분자식 / 분자량** | C10H12N5O7P / 345.21 g/mol |
| **분자 분류** | 퓨린 뉴클레오티드 유도체 / 세포 내 2차 신호전달물질 (Second Messenger) |
| **합성 효소** | 구아닐릴 시클라아제 (Guanylyl Cyclase, GC): 가용성 sGC 및 막결합 pGC |
| **분해 효소** | 포스포디에스테라아제 (Phosphodiesterase, 특히 PDE5, PDE6, PDE9) |
| **주요 작용체** | 단백질 인산화효소 G (PKG), cGMP 개폐형 이온 통로 (CNG channels) |

---

## 2. 주요 조절 본초 및 천연 기원 (Botanical Sources & Content)

> [!warning] ⚠️ 템플릿 적용 상 주의
> cGMP는 식물이 함유하는 파이토케미컬이 아니라 인체 세포가 자체 합성하는 내인성 2차 전달자입니다. 이 절은 "cGMP를 함유하는 본초"가 아니라, **eNOS 발현·NO 생성을 촉진하여 cGMP 축적을 간접적으로 유도하는 것으로 학술 보고된 한약 성분**을 다룹니다.

| 조절 본초 | 유효 성분 | 보고된 작용 |
| :--- | :--- | :--- |
| [[단삼]] | 탄시논 IIA | 혈관 내피 eNOS 발현 유도 → NO 방출 증가 → cGMP 축적 촉진 |
| [[천궁]] | 천궁락톤 | eNOS 활성화를 통한 혈관 확장 |
| [[당귀]] | 페룰산 | 혈관 내피 보호 및 NO-cGMP 경로 촉진 |

---

## 3. 분자약리 표적 & 신호전달 네트워크 (Molecular Targets)

```
              [혈관 내피세포: eNOS 활성화]
                           │
                      [NO 방출]
                           │ (평활근 세포로 확산)
             [가용성 구아닐릴 시클라아제(sGC) 결합]
                           │
                    GTP ───┴───► [[cGMP]] 축적
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  [PKG 활성화]              [PDE5에 의한 분해]
                         │                         │
            세포질 Ca2+ 농도 급감            5'-GMP로 불활성화
            MLCP 활성화 → 미오신 탈인산화       (PDE5 억제 시 cGMP 지속)
                         │
                  [혈관 평활근 이완]
```

1. **합성 경로 (NO-sGC-cGMP Pathway)**: 혈관 내피세포에서 생성된 NO가 평활근 세포막을 확산하여 세포질의 sGC 헴(Heme) 부위에 결합, GTP를 cGMP로 전환시켜 세포 내 농도를 급상승시킵니다.
2. **혈관 평활근 이완 메커니즘**: cGMP는 PKG를 결합·활성화하여 칼슘 채널을 차단하고 SERCA를 자극, 세포질 Ca2+ 농도를 낮춥니다. 미오신 경쇄 인산분해효소(MLCP)를 활성화하여 평활근을 이완·혈관을 확장시킵니다.
3. **분해 및 조절**: cGMP는 PDE5에 의해 5'-GMP로 신속히 가수분해되어 신호가 종결됩니다. 실데나필·타다라필 등은 PDE5를 경쟁적으로 억제하여 cGMP 고농도를 유지시킵니다.

---

## 4. 생체 내 생성·분해 동태 (Pharmacokinetics: ADME 대응)

> [!warning] ⚠️ 템플릿 적용 상 주의
> cGMP는 경구 흡수되는 저분자가 아니므로, 이 절은 **세포 내 cGMP의 생성·분해 회전율** 및 **PDE5 억제제 약물의 실제 약동학**을 함께 다룹니다.

- **초고속 회전율**: 세포 내 cGMP는 PDE(특히 PDE5)에 의해 초 단위로 매우 신속하게 5'-GMP로 분해되어, 자극이 사라지면 농도가 급격히 감소하는 것으로 알려져 있습니다(정확한 조직별 반감기는 세포 유형에 따라 차이가 커 단일 수치로 단정하지 않음).
- **실데나필의 실제 약동학**: 경구 투여 후 약 1시간 내 최고 혈중농도 도달, 반감기 약 3-5시간(제품 정보 기준). 타다라필은 반감기가 약 17.5시간으로 훨씬 길어 지속적인 PDE5 억제 효과를 나타냅니다.

---

## 5. 주요 질환별 약리 효능 & 분자 기전 (Therapeutic Efficacy)

- **발기부전(Erectile Dysfunction)**: 음경 해면체 평활근 내 cGMP 증가를 통해 혈류 유입을 촉진하여 발기 유도.
- **폐동맥 고혈압(Pulmonary Arterial Hypertension)**: 폐혈관 평활근 수축 억제 및 혈관 저항 감소.
- **심부전(Heart Failure)**: sGC 자극제(베리시구앗 Vericiguat)를 통해 cGMP-PKG 경로를 직접 자극하여 심근 재형성 억제 및 혈관 확장.

---

## 6. 조절 본초 방제 시너지 & 배오 매트릭스 (Herbal Synergies)

> [!warning] ⚠️ 템플릿 적용 상 주의
> 아래는 "cGMP를 함유하는 처방"이 아니라, **eNOS-NO-cGMP 경로 촉진이 학술적으로 시사된 활혈거어(活血祛瘀) 처방 배오**입니다.

- **활혈거어약 배오**: [[단삼]](탄시논 IIA), [[천궁]](천궁락톤), [[당귀]](페룰산) 등이 함께 배오되는 [[관심2호방]] 계열 처방에서는 이론적으로 eNOS 발현 촉진의 상가 효과가 가능하다고 추정되나, 처방 수준의 cGMP 상승을 직접 측정한 인체 대조시험은 확인되지 않았습니다.
- **평간식풍약**: [[야국화]](루테올린), [[조구등]](린코필린) 등은 혈압 강하 목적의 처방에서 혈관 평활근 cGMP 경로에 영향을 줄 수 있다고 제시되나, 개별 성분 실험 수준의 근거임을 명시합니다.

---

## 7. 양약 상호작용 & 약물동태학적 간섭 (Drug Interactions)

- **PDE5 억제제 + 질산염(Nitrate) 병용 금기**: 니트로글리세린 등 질산염 제제는 NO를 직접 공급하여 cGMP를 증가시키므로, PDE5 억제제(실데나필 등)와 병용 시 cGMP 분해가 동시에 차단되어 중증 저혈압·심혈관 허탈을 유발할 수 있어 절대 금기입니다.
  - Schwartz BG, Kloner RA. (2010). Drug Interactions With Phosphodiesterase-5 Inhibitors Used for the Treatment of Erectile Dysfunction or Pulmonary Hypertension. *Circulation*, 122(1), 88-95. PMID: 20606131
- **PDE5 억제제 + 리오시구앗(Riociguat, sGC 자극제) 병용 금기**: 두 약물 모두 cGMP 경로를 상승시키는 기전이 중첩되어 저혈압 위험이 증가하므로 병용이 금기되어 있습니다(FDA 제품 라벨 기준).
- **한약재 eNOS 촉진 성분(탄시논 등)과 PDE5 억제제/질산염의 병용에 대한 정량적 인체 상호작용 데이터는 현재 확인되지 않아, 이론적 상가 효과 가능성만 언급하고 단정하지 않습니다.**

---

## 8. 💡 사용자 진료실 핵심 필기 & 임상 응용 팁 (Melt-In & High-Yield)

- 협심증으로 니트로글리세린 설하정을 처방받은 환자에게 실데나필 등 발기부전 치료제를 병용 처방하지 않도록 반드시 확인 — 이는 분자기전(cGMP 이중 축적)에 근거한 절대 금기임을 설명 가능.
- 활혈거어 본초(단삼, 천궁 등)의 "혈액순환 개선" 효능을 NO-cGMP-PKG라는 구체적 분자 경로로 설명하면 이해도를 높일 수 있음.

---

## 9. 출처 및 학술 참고 문헌 (References)

1. Francis, S. H., Busch, J. L., Corbin, J. D., Sibley, D. (2010). cGMP-dependent protein kinases and cGMP phosphodiesterases in nitric oxide and cGMP action. *Pharmacological Reviews*, 62(3): 525-563. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20716671/)
2. Murad, F. (2006). Shattuck Lecture: Nitric oxide and cyclic GMP in cell signaling and drug development. *New England Journal of Medicine*, 355(19): 2003-2011. [PubMed](https://pubmed.ncbi.nlm.nih.gov/17093251/)
3. Schwartz BG, Kloner RA. (2010). Drug Interactions With Phosphodiesterase-5 Inhibitors Used for the Treatment of Erectile Dysfunction or Pulmonary Hypertension. *Circulation*, 122(1), 88-95. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20606131/)

<!-- 보관 태그(1회용·링크오류, 필요시 복원): 2차전달자, 산화질소하류 -->
