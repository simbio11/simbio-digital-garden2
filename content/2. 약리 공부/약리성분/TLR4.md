---
aliases:
  - Toll-Like Receptor 4
  - 톨유사수용체4
  - CD284
tags:
  - 약리성분
  - 수용체
  - 패턴인식수용체
  - 선천면역
  - 신경염증
---

# TLR4 (Toll-Like Receptor 4)

> **핵심 요약 (Key Summary)**:
> 선천면역계의 핵심 패턴인식수용체(PRR)로 그람 음성균의 지질다당류([[LPS]]) 및 내인성 위험 신호(DAMPs)를 감지하는 막관통 수용체.
> MyD88 및 TRIF 경로를 통해 [[NF-κB]]를 전사 활성화하여 전염증성 사이토카인(TNF-α, IL-6, [[COX-2]]) 폭풍을 촉발.
> 청열해독 본초([[황련]], [[청호]])의 과도한 패혈증성 염증 차단 표적이자 [[황기]], [[인삼]] 다당체의 온화한 면역 증강(부정거사) 표적.

---

## 1. 기본 화학 정보 & 분자 구조식 (Chemical Identity)

> [!info] 🧪 3D 뷰어 미적용
> TLR4는 소분자가 아닌 막단백질 수용체라 PubChem 소분자 CID가 없습니다. UniProt [O00206](https://www.uniprot.org/uniprotkb/O00206)로 확인하세요.

| 항목 | 내용 |
| :--- | :--- |
| **수용체명** | TLR4 (Toll-Like Receptor 4, CD284) |
| **분자량** | 약 95~110 kDa (당화 막관통 단백질) |
| **유전자 위치** | 9q33.1 (인간 *TLR4* 유전자) |
| **주요 발현 세포** | 대식세포, 수지상세포, 뇌 미세아교세포(Microglia), 혈관 내피세포 |
| **대표 리간드** | 외인성 [[LPS]](엔도톡신), 내인성 HMGB1, Hsp70, 포화지방산, 식물 다당체 |
| **약리 분류** | 패턴인식수용체(PRR), 선천면역 스위치, 신경염증 및 패혈증 분자 표적 |

---

## 2. 주요 조절 본초 및 천연 기원 (Botanical Sources & Content)

> [!warning] ⚠️ 템플릿 적용 상 주의
> TLR4는 식물이 함유하는 파이토케미컬이 아니라 인체 면역세포가 발현하는 내인성 막수용체입니다. 이 절은 "TLR4를 함유하는 본초"가 아니라, **TLR4 신호를 차단하거나(길항) 온화하게 자극하는(효능제 유사) 것으로 학술 보고된 한약 성분**을 다룹니다.

| 조절 본초 | 유효 성분 | 보고된 작용 |
| :--- | :--- | :--- |
| [[황련]] | [[베르베린]] | TLR4/MD-2 복합체 결합 경쟁적 차단 (길항) |
| [[황금]] | [[바이칼레인]] | TLR4 하류 신호 억제 |
| [[청호]] | [[아르테미시닌]] | TLR4 매개 염증 반응 억제 |
| [[황기]] | 황기다당체(APS) | TLR4 온화한 자극을 통한 대식세포 항원제시능 강화 |
| [[인삼]] | 진세노사이드 다당체 분획 | TLR4 매개 면역 증강 |

---

## 3. 분자약리 표적 & 신호전달 네트워크 (Molecular Targets)

```
[TLR4 이량체화 및 이중 신호전달 캐스케이드]
       LPS / 내독소 / DAMPs (위험신호)
                 │
                 ▼
       LBP (LPS 결합 단백질) ──► CD14
                 │
                 ▼
       TLR4 / MD-2 수용체 복합체 이량체화
                 │
     ┌───────────┴───────────┐
     ▼                       ▼
  [MyD88 의존성 경로]     [TRIF 의존성 경로]
  (세포막 조기 반응)      (엔도솜 후기 반응)
     │                       │
  IRAK4 / IRAK1           TRAM / TRIF
     │                       │
   TRAF6                   TBK1 / IKKε
     │                       │
   TAK1 ──► IKK 복합체     IRF3 인산화 & 핵 전위
     │        │              │
     │        ▼              ▼
     │   IκBα 분해       [Type I 인터페론 (IFN-β)]
     │        │          (항바이러스 선천면역)
     │        ▼
     └─► [[NF-κB]] 핵 전위
              │
              ▼
  [전염증성 사이토카인 폭풍]
  TNF-α, IL-1β, IL-6, [[COX-2]], iNOS
```

- **MyD88 의존 경로**: TLR4 이량체화 후 MyD88 어댑터 단백질이 결합하여 IκBα를 분해하고 NF-κB를 세포핵으로 이동시켜 급성 염증 매개인자를 폭발적으로 분비시킵니다.
- **TRIF 의존 경로**: 세포막에서 엔도솜으로 내재화된 TLR4는 TRIF를 통해 IRF3을 활성화하여 제1형 인터페론을 방출합니다. 이 TRIF 신호는 TLR4가 세포막에서 엔도솜으로 이동(internalization)해야만 개시되는 것으로 규명되어 있습니다 (Kagan 2008).

---

## 4. 수용체 내재화·분해 동태 (Pharmacokinetics: ADME 대응)

> [!warning] ⚠️ 템플릿 적용 상 주의
> TLR4 자체는 경구 흡수·간대사되는 저분자가 아니므로, 이 절은 **수용체 단백질의 세포 내 이동(trafficking)과 신호 종결 동태**를 다룹니다.

- **리간드 유도 내재화**: LPS 결합 후 TLR4/MD-2 복합체는 CD14 의존적으로 세포막에서 엔도솜으로 내재화되며, 이 과정에서 신호가 MyD88(막) 우세에서 TRIF(엔도솜) 우세로 전환됩니다 (Kagan 2008, *Nature Immunology*).
- **신호 종결**: 엔도솜 내재화 이후 TLR4는 분해되거나 재순환(recycling)되어 지속적 과잉 자극을 방지하는 것으로 알려져 있으나, 정량적 반감기 수치는 세포 유형별 차이가 커 이 노트에서 단일 수치로 단정하지 않습니다.

---

## 5. 주요 질환별 약리 효능 & 분자 기전 (Therapeutic Efficacy)

- **신경병증성 통증 및 척수 감작**: 손상 신경 주위 미세아교세포의 TLR4가 활성화되면 만성 난치성 통증을 유발.
- **비알코올성 지방간(NAFLD) 및 인슐린 저항성**: 장관 누수로 유입된 내독소가 간 쿠퍼세포의 TLR4를 자극하여 지방간염을 유발.
- **패혈증**: 전신 LPS 노출에 의한 TLR4 과활성화가 사이토카인 폭풍과 다발성 장기부전의 핵심 기전.

---

## 6. 조절 본초 방제 시너지 & 배오 매트릭스 (Herbal Synergies)

> [!warning] ⚠️ 템플릿 적용 상 주의
> 아래는 "TLR4를 함유하는 처방"이 아니라, **TLR4 경로의 양면적(차단/자극) 조절이 학술적으로 보고된 처방 배오**입니다.

- **청열해독(淸熱解毒) 방향**: [[황련해독탕]] 등에서 [[황련]](베르베린)·[[황금]](바이칼레인)·[[청호]](아르테미시닌)이 함께 배오되어 TLR4/MD-2 결합을 경쟁적으로 차단, 전신 염증과 뇌 미세아교세포 흥분을 억제하는 방향으로 작용한다고 보고됩니다.
- **보기부정(補氣扶正) 방향**: [[황기]]와 [[인삼]]이 함께 배오되는 보익 처방(예: [[보중익기탕]])에서는 다당체 성분이 TLR4를 온화하게 자극하여 면역 감시 기능을 강화하는 반대 방향의 조절이 보고되어, 동일 수용체에 대한 "차단 vs 자극"이라는 처방 전략상의 양면성을 보여줍니다.

---

## 7. 양약 상호작용 & 약물동태학적 간섭 (Drug Interactions)

- **에리토란(Eritoran, TLR4/MD-2 길항제)**: 중증 패혈증 치료 목적으로 개발된 합성 TLR4 길항제로, 대규모 3상 ACCESS 무작위 임상시험에서 위약 대비 28일·1년 사망률 감소 효과를 입증하지 못하고 임상 개발이 중단되었습니다. 이는 TLR4 단일 표적 차단만으로는 복합적인 패혈증 병태생리를 해결하기 어렵다는 것을 보여준 대표적 사례입니다.
  - Opal SM, et al. Effect of eritoran, an antagonist of MD2-TLR4, on mortality in patients with severe sepsis: the ACCESS randomized trial. *JAMA*. 2013. PMID: 23512062
- 한약재 TLR4 조절 성분(베르베린 등)과 에리토란 같은 표적 약물이 임상에서 병용된 사례나 상호작용 데이터는 현재 확인되지 않습니다.

---

## 8. 💡 사용자 진료실 핵심 필기 & 임상 응용 팁 (Melt-In & High-Yield)

- 동일 수용체(TLR4)라도 "과도한 염증을 끄는 것"(황련해독탕 계열)과 "면역을 깨우는 것"(보중익기탕 계열)이라는 정반대 임상 전략에 쓰일 수 있음을 이해하면 변증 논리를 분자약리로 설명 가능.
- 에리토란의 임상 실패 사례는 "단일 분자표적 차단제"의 한계를 설명하며, 다중 표적을 겨냥하는 복합 처방의 이론적 근거로 활용 가능(단, 처방 수준의 임상적 우월성이 입증된 것은 아님을 함께 설명해야 함).

---

## 9. 출처 및 학술 참고 문헌 (References)

1. Medzhitov R, et al. (1997). A human homologue of the Drosophila Toll protein signals activation of adaptive immunity. *Nature*, 388(6640), 394-397. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9237759/)
2. Lu YC, et al. (2008). LPS/TLR4 signal transduction pathway. *Cytokine*, 42(2), 145-151. [PubMed](https://pubmed.ncbi.nlm.nih.gov/18304834/)
3. Kagan JC, et al. (2008). TRAM couples endocytosis of Toll-like receptor 4 to the induction of interferon-β. *Nature Immunology*, 9(4), 361-368. [PubMed](https://pubmed.ncbi.nlm.nih.gov/18297073/)
4. Opal SM, et al. (2013). Effect of eritoran, an antagonist of MD2-TLR4, on mortality in patients with severe sepsis: the ACCESS randomized trial. *JAMA*, 309(11), 1154-1162. [PubMed](https://pubmed.ncbi.nlm.nih.gov/23512062/)
