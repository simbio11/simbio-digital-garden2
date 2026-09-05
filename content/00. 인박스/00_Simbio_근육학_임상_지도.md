# 🗺️ Simbio 임상 근육학 통합 지도 (Clinical Muscle Master Map)

> **임상 진료 대시보드 v1.0** | 인체 부위별·질환별·기능 사슬별 원클릭 통합 네비게이터  
> **빠른 이동**: [[#1. 🧍 인터랙티브 인체 지도 (Interactive Body Map)|인체 지도]] | [[#2. 🩺 임상 질환별 원클릭 치료 세트 (Clinical Syndromes)|질환별 세트]] | [[#3. ⚡ 짝힘(Force Couple) & 기능 사슬 맵 (Kinetic Chains)|기능 사슬]] | [[#4. 💎 원장님 특화 임상 노트 & 감별 진단 슬롯|원장님 필기]]

---

## 1. 🧍 인터랙티브 인체 지도 (Interactive Body Map)

<div style="background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 12px; padding: 20px; border: 1px solid #334155; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); margin-bottom: 25px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
    <h3 style="margin: 0; color: #38bdf8; font-size: 18px;">🎯 인체 부위별 빠른 진입 (Quick Regional Access)</h3>
    <span style="font-size: 12px; color: #94a3b8;">부위 박스를 클릭하면 해당 상세 치료 모듈로 즉시 점프합니다</span>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
    
    <!-- 두경부 -->
    <a href="#2-1-두경부턱관절-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #0284c7; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#0369a1'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #38bdf8; font-size: 14px;">🧠 두경부 & 턱관절</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[흉쇄유돌근]] · [[사각근]] · [[후두하근]] · [[교근]]</div>
        <div style="font-size: 10px; color: #38bdf8; margin-top: 6px;">경추성두통 / TMJ / 흉곽출구 →</div>
      </div>
    </a>

    <!-- 견배부/상지 -->
    <a href="#2-2-어깨상지-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #0d9488; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#0f766e'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #2dd4bf; font-size: 14px;">💪 견배부 & 상지</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[극상근]] · [[견갑하근]] · [[소흉근]] · [[회외근]]</div>
        <div style="font-size: 10px; color: #2dd4bf; margin-top: 6px;">오십견 / 회전근개 / 테니스엘보 →</div>
      </div>
    </a>

    <!-- 흉요추/코어 -->
    <a href="#2-3-요통골반-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #ca8a04; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#a16207'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #facc15; font-size: 14px;">⚡ 흉요추 & 코어</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[장요근]] · [[요방형근]] · [[다열근]] · [[복횡근]]</div>
        <div style="font-size: 10px; color: #facc15; margin-top: 6px;">급만성 요통 / 디스크 / 골반틀어짐 →</div>
      </div>
    </a>

    <!-- 둔부/고관절 -->
    <a href="#2-4-둔부고관절-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #ea580c; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#c2410c'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #fb923c; font-size: 14px;">🍑 둔부 & 고관절</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[중둔근]] · [[이상근]] · [[대퇴근막장근(TFL)]] · [[내전근]]</div>
        <div style="font-size: 10px; color: #fb923c; margin-top: 6px;">이상근증후군 / 대전자점액낭 / 서혜부통 →</div>
      </div>
    </a>

    <!-- 무릎/하지 -->
    <a href="#2-5-슬관절하지-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #db2777; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#be185d'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #f472b6; font-size: 14px;">🦵 슬관절 & 하지</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[대퇴직근]] · [[슬와근]] · [[반막양근]] · [[비복근]]</div>
        <div style="font-size: 10px; color: #f472b6; margin-top: 6px;">PFPS / 베이커낭종 / 테니스레그 →</div>
      </div>
    </a>

    <!-- 발목/족부 -->
    <a href="#2-6-발목족부-질환군" style="text-decoration: none;">
      <div style="background: #1e293b; border: 1px solid #7c3aed; border-radius: 8px; padding: 12px; transition: all 0.2s; cursor: pointer;" onmouseover="this.style.background='#6d28d9'; this.style.transform='translateY(-2px)';" onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';">
        <div style="font-weight: bold; color: #a78bfa; font-size: 14px;">🦶 발목 & 족부</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">[[전경골근]] · [[후경골근]] · [[장비골근]] · [[장지신근]]</div>
        <div style="font-size: 10px; color: #a78bfa; margin-top: 6px;">족저근막염 / 만성염좌 / 신스프린트 →</div>
      </div>
    </a>

  </div>
</div>

---

## 2. 🩺 임상 질환별 원클릭 치료 세트 (Clinical Syndromes)

> 임상에서 환자가 주소증(Chief Complaint)을 호소할 때, **어떤 근육들을 한 세트로 묶어서 자침·약침·도침·추나 치료해야 하는지**를 일목요연하게 정리한 실전 프로토콜입니다.

### 2-1. 두경부·턱관절 질환군

#### 1) 흉곽출구증후군 (Thoracic Outlet Syndrome, TOS)
* **핵심 병변근 세트**: [[전사각근]] + [[중사각근]] + [[소흉근]] + [[쇄골하근]]
* **동반 보상/안정근**: [[견갑거근]], [[상부승모근]], [[능형근]]
* **임상 접근 포인트**:
  * 사각근 삼각(Scalene triangle) 완화 $\rightarrow$ 완신경총 및 쇄골하동맥 감압.
  * 소흉근 하부 오훼돌기 부착부 도침 박리술 $\rightarrow$ 늑쇄간극 확보.
  > [!NOTE] 💎 원장님 임상 필기 슬롯 (TOS)
  > 팔 저림이 4-5지로 올 때 경추 디스크(C8)와 사각근 포착 감별. 사각근 자침 후 소흉근 부착부(오훼돌기 내하방 1촌) 약침 시 저림 즉각 호전.

#### 2) 경추성 두통 & 후두신경통 (Cervicogenic Headache)
* **핵심 병변근 세트**: [[후두하근]]([[대후두직근]], [[하두사근]]) + [[두판상근]] + [[두반극근]] + [[상부승모근]]
* **임상 접근 포인트**:
  * 제2경추 극돌기(C2) $\sim$ 후두골 상항선 라인의 대후두신경 통과 지점 집중 자침(풍지·천주·완골).

#### 3) 턱관절 장애 & 개구장애 (TMJ Dysfunction)
* **핵심 병변근 세트**: [[외익상근]] + [[내익상근]] + [[교근]] + [[측두근]] + [[이복근]]
* **임상 접근 포인트**:
  * 입을 벌릴 때 턱이 지그재그로 틀어지면 외익상근 외측두 불균형 교정.

---

### 2-2. 어깨·상지 질환군

#### 1) 동결견 / 오십견 (Frozen Shoulder / Adhesive Capsulitis)
* **핵심 병변근 세트**: [[견갑하근]] + [[소원근]] + [[오훼완근]] + [[극하근]] + [[광배근]]
* **임상 접근 포인트**:
  * **외회전 제한의 절대 주범**: [[견갑하근]] 액와 하부 부착부 박리.
  * **열중쉬어(내회전) 제한 주범**: [[극하근]], [[소원근]], 후관절낭 유착.

#### 2) 충돌증후군 & 극상근건염 (Subacromial Impingement)
* **핵심 병변근 세트**: [[극상근]] + [[삼각근]] + [[상완이두근]](장두) + [[전거근]] + [[하부승모근]]
* **임상 접근 포인트**:
  * 삼각근의 과도한 상방 당김에 대항하여 극상근과 견갑하근의 상완골두 하방 안정화 회복.

#### 3) 외측상과염 / 테니스엘보 (Lateral Epicondylalgia)
* **핵심 병변근 세트**: [[단요측수근신근]] + [[회외근]] + [[수지신근]] + [[상완요골근]] + [[상완삼두근]](외측두)`
* **임상 접근 포인트**:
  * 외측상과 총신근건 부착부 도침술 + 회외근의 후골간신경(PIN) 감압 자침(곡지·수삼리).

---

### 2-3. 요통·골반 질환군

#### 1) 급성 요추 염좌 & 요방형근 증후군 (Acute Lumbar Sprain)
* **핵심 병변근 세트**: [[요방형근]] + [[장요근]] + [[둔근]]([[중둔근]])` + [[다열근(요부)]] + [[복사근]]
* **임상 접근 포인트**:
  * 장골능 $\sim$ 12번 늑골 사이 요방형근 심부 TP(지실·신수 외측) 자침 + 장골근 압통점 이완.

#### 2) 요추 추간판 탈출증 (HIVD / Lumbar Herniation)
* **핵심 병변근 세트**: [[다열근(요부)]] + [[장요근]] + [[슬괵근]] + [[대둔근]] + [[이상근]]
* **신경근 분절 지표 매핑**:
  * **L4**: [[전경골근]] 근력 저하 (발목 배굴)
  * **L5**: [[장모지신근]] 근력 저하 (엄지발가락 신전)
  * **S1**: [[비복근]], [[가자미근]] 근력 저하 (까치발 저측굴곡)

---

### 2-4. 둔부·고관절 질환군

#### 1) 이상근증후군 & 좌골신경통 (Piriformis Syndrome)
* **핵심 병변근 세트**: [[이상근]] + [[상쌍자근]] + [[하쌍자근]] + [[내폐쇄근]] + [[대퇴방형근]] + [[대둔근]]
* **임상 접근 포인트**:
  * 대퇴골 대전자 $\sim$ 천골 외측연을 잇는 이상근 주행선 중앙 심부 직자(환도혈 60~75mm) 좌골신경 감압.

#### 2) 대퇴비구충돌 & 서혜부 통증 (FAI / Groin Pain)
* **핵심 병변근 세트**: [[장내전근]] + [[치골근]] + [[장요근]] + [[대퇴직근]] + [[봉공근]]
* **임상 접근 포인트**:
  * 대퇴삼각(Femoral triangle) 및 치골 결합 부착부 건병증 도침 이완술.

---

### 2-5. 슬관절·하지 질환군

#### 1) 슬개대퇴통증증후군 (PFPS / Jumper's Knee)
* **핵심 병변근 세트**: [[외측광근]] + [[대퇴근막장근(TFL)]] + [[내측광근]](VMO) + [[대퇴직근]] + [[중둔근]]
* **임상 접근 포인트**:
  * 외측광근/ITB의 과긴장으로 슬개골이 외측으로 편위 $\rightarrow$ VMO 강화 및 외측 지대 도침 감압.

#### 2) 베이커 낭종 & 오금 통증 (Baker's Cyst & Popliteal Pain)
* **핵심 병변근 세트**: [[반막양근]] + [[비복근]](내측두)` + [[슬와근]] + [[대퇴이두근]]
* **임상 접근 포인트**:
  * 반막양근-비복근 점액낭 압력 감소를 위해 내측 햄스트링 및 비복근 기시부 집중 치료(위중·음곡).

---

### 2-6. 발목·족부 질환군

#### 1) 족저근막염 & 발뒤꿈치 통증 (Plantar Fasciitis)
* **핵심 병변근 세트**: [[비복근]] + [[가자미근]] + [[전경골근]] + [[장지신근]] + [[단지굴근(발)]] + [[후경골근]]
* **연쇄 사슬 메커니즘**:
  * 전경골근 약화 $\rightarrow$ 장지신근 과부하 $\rightarrow$ 족저근막 견인 $\rightarrow$ 종골 부착부 염증.

#### 2) 만성 발목 불안정증 & 외측 염좌 (Chronic Ankle Instability)
* **핵심 병변근 세트**: [[단비골근]] + [[장비골근]] + [[제3비골근]] + [[전거비인대]] + [[후경골근]]
* **임상 접근 포인트**:
  * 외과 후방 비골근 건초 도침술 및 단비골근 근력 강화로 내번 염좌 재발 차단.

---

## 3. ⚡ 짝힘(Force Couple) & 기능 사슬 맵 (Kinetic Chains)

### 3-1. 견갑골 3대 상방회전 짝힘 (Scapular Upward Rotation Couple)
> 팔을 위로 180° 들어올릴 때 완벽한 견봉하 공간을 확보하는 3대 협동근

```
        [ 상부승모근 ] (쇄골/견봉 상방 견인)
               ▲
               │
[ 전거근 ] ────┼──── [ 하부승모근 ] (견갑하각 외측 및 내하방 고정)
(하각 전외측 견인)
```
* **치료 타깃**: 어깨 충돌 시 **전거근 약화 + 상부승모근 과긴장** 패턴 교정 필수.

---

### 3-2. 골반 전·후방 경사 짝힘 (Pelvic Tilt Force Couples)

| 골반 경사 유형 | 단축/과긴장 근육군 (치료/자침/이완) | 약화/신장 근육군 (강화/활성화) | 임상 질환 연계 |
| :--- | :--- | :--- | :--- |
| **전방경사 (Anterior Tilt)**<br>*(오리궁둥이/Lordosis)* | [[장요근]], [[대퇴직근]], [[척추기립근]](요장늑근)` | [[복직근]], [[대둔근]], [[슬괵근]] | 요추 전만증, 파셋관절염, 척추전방전위증 |
| **후방경사 (Posterior Tilt)**<br>*(일자허리/Flat back)* | [[대둔근]], [[슬괵근]], [[복직근]] | [[장요근]], [[척추기립근]], [[대퇴사두근]] | 요추 디스크 탈출증, 흉요추 후만, 거북목 |

---

### 3-3. 발바닥 아치 슬링 짝힘 (Foot Stirrup Force Couple)
* **내측 거상 슬링**: [[전경골근]] (발등 내측 상방 견인) $\longleftrightarrow$ [[장비골근]] (발바닥 외측 $\rightarrow$ 내측 하방 견인)
* **내외측 아치 균형**: 두 근육이 제1중족골 기저부에서 교차하며 발의 횡아치(Transverse arch)를 팽팽한 활처럼 지지.

---

## 4. 💎 원장님 특화 임상 노트 & 감별 진단 슬롯

> [!TIP] 📝 원장님 전용 임상 필기 추가 가이드
> 진료 중 발견하신 새로운 근육 연계 패턴이나 약침 배합 노하우, 환자 티칭 팁을 아래 블록에 자유롭게 추가해 주세요!

```markdown
> [!NOTE] 💎 [원장님 임상 보물창고]: 슬관절 내측 통증 감별 팁
> 1. 거위발건염(봉공근·박근·반건양근): 경골 조면 내측 2cm 하방 압통.
> 2. 내측 반월판 파열: 관절열극(Joint line) 정확한 압통 및 McMurray 양성.
> 3. 복재신경 포착: 헌터관(내전근관) 압통 시 슬내측 시린 느낌 방사.
```

---

## 🧭 볼트 지식 빠른 이동
* [[c:\Simbio\00_Simbio_프로젝트_대시보드.md|📊 Simbio 볼트 종합 대시보드]]
* [[1. 근골격계 공부/00_근골격계_MOC|📚 근골격계 MOC (전체 172개 근육 색인)]]
* [[00_근막경선해부학_MOC|🔗 근막경선해부학 MOC]]
