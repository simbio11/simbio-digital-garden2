---
title: P-당단백(P-gp)
created: 2026-09-10
updated: 2026-11-15
tags:
  - 이론
  - 개념사전
  - 약물상호작용
  - 수송체
  - ABCB1
출처: "PubMed, UniProt"
aliases:
  - P-glycoprotein
  - P-gp
  - ABCB1
  - MDR1
  - 다약제내성단백
type: 의학개념
category: "_의학/03_이론/의학개념/분자·세포 기전/02_효소·대사경로"
---

# 🧬 [[P-당단백(P-gp)]] (P-glycoprotein, ABCB1 / MDR1)

> **핵심 요약 (Key Summary)**:
> - **분자 정체**: *ABCB1*(MDR1) 유전자가 암호화하는 ATP 의존성 약물 유출(Efflux) 펌프(약 170 kDa, ABC 수송체 슈퍼패밀리). 소장 상피·[[혈뇌장벽]](BBB)·신세뇨관·간 담세관·태반에 분포해 이물질과 기질 약물을 세포 밖으로 능동 배출함.
> - **약동학적 역할**: 대사 효소 [[CYP3A4]]와 **[[PXR]]/[[CAR]]** 전사 조절계를 공유하며, 경구 약물의 **1차 통과(First-pass) 생체이용률**과 중추신경계 투과도를 결정하는 핵심 관문임.
> - **유도 vs 억제**: 장관 P-gp가 **유도**되면 기질 약물의 Cmax·AUC가 하락(약효 저하)하고, **억제**되면 체내 축적 및 뇌 투과 증가로 독성이 유발됨.
> - **한의·임상 실증**: [[반하백출천마탕]]·[[황련해독탕]] 병용 시 [[에독사반]] Cmax 18.5~28.1% 감소(장관 P-gp 유도 해석), [[황련]]([[베르베린]])의 P-gp 기질/억제 이중성, 상용 상호작용 DB에서 **수송체 축(P-gp·[[SLCO1B1]])**이 CYP 대비 과소평가되는 한계에 유의해야 함.

---

## 📌 목차
1. [분자 구조 및 조직 분포 (Molecular Architecture & Tissue Localization)](#1-분자-구조-및-조직-분포-molecular-architecture--tissue-localization)
2. [유출 기전 및 CYP3A4·OATP 수송체 축 비교 (Efflux Mechanism & Transporter Axis)](#2-유출-기전-및-cyp3a4oatp-수송체-축-비교-efflux-mechanism--transporter-axis)
3. [대표 기질·유도제·억제제 (Substrates, Inducers & Inhibitors)](#3-대표-기질유도제억제제-substrates-inducers--inhibitors)
4. [한의학적 연계: 한약-DOAC·베르베린 상호작용 실증 (Integrative Korean Medicine)](#4-한의학적-연계-한약-doac베르베린-상호작용-실증-integrative-korean-medicine)
5. [임상 해석 한계: DB 불일치와 수송체 축 누락 주의 (Clinical Pitfalls & DB Concordance)](#5-임상-해석-한계-db-불일치와-수송체-축-누락-주의-clinical-pitfalls--db-concordance)
6. [💡 사용자 진료실 핵심 필기 & 실전 임상 체크리스트](#6--사용자-진료실-핵심-필기--실전-임상-체크리스트)
7. [출처 및 학술 참고 문헌 (References)](#7-출처-및-학술-참고-문헌-references)

---

## 1. 분자 구조 및 조직 분포 (Molecular Architecture & Tissue Localization)

* **구조**: 2개의 막통과 도메인(TMD, 각 6회 막관통 $\alpha$-나선)과 2개의 세포질 내 뉴클레오타이드 결합 도메인(NBD)으로 구성된 약 170 kDa 당단백질입니다(Callaghan et al. 2020). ATP 가수분해 에너지를 이용해 소수성·양친매성 기질을 세포막 지질 이중층에서 직접 포집해 세포 외로 펌프질합니다.

| 발현 조직 | 세포막 위치 | 생리적·약동학적 방향 |
| :--- | :--- | :--- |
| **소장 상피세포** | 장측막 (Apical membrane) | 약물을 장관 내강으로 되돌려 배출 $\rightarrow$ **경구 흡수율(Cmax/AUC) 제한** |
| **[[혈뇌장벽]](BBB)** | 뇌 모세혈관 내피세포 내강측 | 약물의 뇌 실질 유입 차단 $\rightarrow$ 중추 신경독성 방어 (Chai et al. 2022) |
| **신장 근위세뇨관** | 요세관 내강측 | 혈중 기질 약물·대사체의 **소변 배설 촉진** |
| **간세포** | 담세관막 (Canalicular membrane) | 약물·담즙 성분의 **담즙 배설 촉진** |
| **태반 합포체영양막** | 모체 혈액측 | 모체 복용 약물로부터 **태아 노출 보호** |

---

## 2. 유출 기전 및 CYP3A4·OATP 수송체 축 비교 (Efflux Mechanism & Transporter Axis)

```
[경구 기질 약물] ──► (소장 상피세포 유입)
                         │
      ┌──────────────────┴──────────────────┐
      ▼                                     ▼
 [장관 P-gp 유출]                     [문맥 → 간세포 유입]
 내강으로 역배출                       [[SLCO1B1]](OATP1B1) 등 유입 수송체
      │                                     │
      ▼                                     ▼
  흡수량(Cmax) 조절                   간 내 [[CYP3A4]] 대사 및 담즙 배설
```

* **유출 축 vs 유입 축의 분리 (Aebi et al. 2025; Balasubramanian 2021)**:
  - **유출(Efflux) 축**: P-gp(ABCB1)와 BCRP가 장관 흡수를 제한하고 담즙/요 배설을 촉진합니다.
  - **유입(Uptake) 축**: 스타틴의 간세포 유입은 **[[SLCO1B1]](OATP1B1)**이 담당합니다. 유입 수송체 변이나 억제제([[사이클로스포린]], 젬피브로질) 병용 시 간으로 들어가지 못한 스타틴의 혈중 농도가 급등해 **[[스타틴 유발 근병증]](SAMS)** 위험이 커집니다.

---

## 3. 대표 기질·유도제·억제제 (Substrates, Inducers & Inhibitors)

| 구분 | 대표 약물 및 물질 | 임상적 주의 포인트 |
| :--- | :--- | :--- |
| **핵심 기질 (Substrates)** | [[디곡신]], **DOAC([[에독사반]], [[아픽사반]], [[리바록사반]], 다비가트란)**, [[콜히친]], [[타크로리무스]], [[사이클로스포린]], [[로페라미드]], 일부 [[스타틴]], [[베르베린]] | 디곡신·로페라미드처럼 대사되지 않는 순수 P-gp 기질은 P-gp 억제 시 즉각 혈중/뇌 농도 급등 |
| **유도제 (Inducers)** | [[리팜핀]], **[[세인트존스워트]]([[hyperforin|하이퍼포린]])**, 카바마제핀, 페니토인 | [[PXR]] 경유 전사 증가 $\rightarrow$ 기질 약물 흡수 저하 및 치료 실패 |
| **억제제 (Inhibitors)** | 아미오다론, 베라파밀, 퀴니딘, 클라리트로마이신, 이트라코나졸, 사이클로스포린 | P-gp 차단 $\rightarrow$ 디곡신 중독(부정맥), 콜히친 독성, DOAC 출혈 위험 |

---

## 4. 한의학적 연계: 한약-DOAC·베르베린 상호작용 실증 (Integrative Korean Medicine)

1. **[[반하백출천마탕]]·[[황련해독탕]]과 [[에독사반]] 병용 임상시험 (Cho et al. 2025)**:
   - 건강인 6일 병용 연구에서 에독사반의 **AUC는 불변이었으나 Cmax가 18.5~28.1% 감소**했고, 약력학 지표([[aPTT와 PT]])는 동등하게 유지되었습니다. 저자들은 이를 대사 효소 억제가 아닌 **장관 P-gp 유도**에 따른 흡수상(Absorption phase) 변화로 해석했습니다.
2. **[[황련]] ([[베르베린]])의 이중성**:
   - 베르베린은 P-gp의 기질이면서 동시에 억제 작용도 보고되어 있어, 황련 함유 처방과 DOAC·디곡신 등 P-gp 기질을 병용할 때는 노출 변화 가능성을 염두에 두어야 합니다.
3. **OATP1B1 억제 해석의 경계 (Aebi et al. 2025)**:
   - 본초 성분의 OATP1B1 억제는 현재까지 주로 시험관 보고 수준이며 임상 용량에서의 의의는 확립되지 않았으므로, 근거 밖 단정을 피하고 임상 지표(CK, 근육통 등) 모니터링으로 대응합니다.

---

## 5. 임상 해석 한계: DB 불일치와 수송체 축 누락 주의 (Clinical Pitfalls & DB Concordance)

* **상용 상호작용 DB의 구조적 맹점 (Phan et al. 2026)**: 4개 주요 상호작용 DB(Micromedex·Lexicomp·Medscape·Stockley's)의 일치도가 kappa -0.0653(완전 일치 0.7%)에 불과한 이유 중 하나는, 상용 DB 항목이 CYP 대사에 편중되어 **장관 P-gp, [[SLCO1B1]](OATP), OCT([[메트포르민]] 배설) 같은 수송체 축을 과소평가**하기 때문입니다(예: [[아토르바스타틴]]의 OATP1B1, [[클로피도그렐]]의 P-gp 흡수 단계).
* **조직별·지표별 괴리**: 장관 P-gp 변화는 Cmax만 변하고 AUC나 약력학(PD)은 유지되는 패턴으로 나타날 수 있으며, 시험관(in vitro) 억제/유도 결과를 임상 용량으로 그대로 외삽해서는 안 됩니다.

---

## 6. 💡 사용자 진료실 핵심 필기 & 실전 임상 체크리스트

> [!tip] 진료실 수송체 기반 병용 안전 수칙 (심층리뷰 통합)
> 1. **"CYP 목록에 없음 = 안전" 착각 금지**: 상호작용 점검 시 대사([[CYP3A4]])뿐만 아니라 **유출 수송체(P-gp)**와 **유입 수송체([[SLCO1B1]])** 축을 반드시 별도 층위로 확인합니다.
> 2. **순수 P-gp 기질 주의**: [[디곡신]], [[콜히친]], 다비가트란, [[에독사반]] 복용 환자가 [[세인트존스워트]] 등 P-gp 유도성 보충제를 복용하지 않도록 교육하고, 한약 병용 시작·중단 시 **2주 내외로 임상 증상(서맥·오심·출혈·맥박/혈압) 모니터링**을 시행합니다.
> 3. **스타틴 근병증 상담**: 스타틴 복용 환자의 근육통 호소 시 단순 약물 부작용 외에 [[SLCO1B1]] 유전형이나 유입 수송체 억제 병용약 유무를 함께 살핍니다.
> - 관련 심층 노트: [[2026-09-10_통합의학약리학_심층리뷰]] · [[2026-11-05_통합의학약리학_개념학습]] · [[2026-11-12_통합의학약리학_심층리뷰]] · [[한약-양약 상호작용]]

---

## 7. 출처 및 학술 참고 문헌 (References)

1. Callaghan R, et al. (2020). Mamma Mia, P-glycoprotein binds again. *FEBS Lett*, 594(23):4076-4084. PMID: 33022784
   - **핵심 요약**: P-당단백(ABCB1)의 막관통 구조, ATP 가수분해 연계 약물 포집·유출 동역학 및 다약제 내성 기전을 해설한 종설.
2. Chai AB, et al. (2022). Regulation of P-Glycoprotein in the Brain. *Int J Mol Sci*, 23(23):14667. PMID: 36498995
   - **핵심 요약**: 혈뇌장벽(BBB)에서 P-당단백의 발현 조절 기전(PXR/CAR 등)과 중추신경계 약물 투과도 제어 역할을 정리한 종설.
3. Cho SJ, et al. (2025). Impact of Banhabaekchulcheonmatang (Banxia Baizhu Tianma Tang) and Hwangryeonhaedoktang (Huang Lian Jie Du Tang) on edoxaban: Herb-drug interaction study in healthy subjects. *J Ethnopharmacol*, 337(Pt 3):118997. PMID: 39461388
   - **핵심 요약**: 반하백출천마탕·황련해독탕 병용 시 에독사반 AUC 불변·Cmax 감소 현상을 장관 P-gp 유도로 해석한 인체 약동학 연구.
4. Phan ADT, et al. (2026). Herbal medicine use disclosure, database-flagged potential herb-drug interactions, and inter - interaction database concordance among patients with non-communicable diseases in Vietnam: A multicenter cross-sectional study. *PLoS One*, 21(7):e0355046. PMID: 42536629
   - **핵심 요약**: 4개 상용 DB의 불일치 원인과 CYP 외 수송체 축(P-gp, OATP) 평가의 중요성을 제시한 다기관 연구.
5. Aebi PS, et al. (2025). Safety outcomes of statin vs non-statin lipid-lowering interventions in patients with prior statin-associated muscle symptoms: A systematic review and meta-analysis. *PLoS One*, 20(12):e0338575. PMID: 41379822
   - **핵심 요약**: 스타틴 유발 근육 증상(SAMS)과 SLCO1B1(OATP1B1) 수송체 변이 및 비스타틴 대안 치료의 안전성을 분석한 메타분석.

<!-- 보관 태그(1회용·링크오류, 필요시 복원): 약물수송체, ABCB1, MDR1, 유출펌프 -->
