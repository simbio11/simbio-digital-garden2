const fs = require('fs');
const path = require('path');

const srcPath = 'c:/Simbio/_AI_OS/30_Sprint_Logs/미노트화_링크_목록.md';

const COMPLETED_BATCH_3 = new Set([
    // 이전 생성 확인 및 alias 매핑 완료
    '연하장애', '중수골', '고혈압', '역류성 식도염', '비골', '종골',
    '흉추', '늑골', '고지혈증', '장골', '라운드 숄더', 'CGRP', 'substance P',
    '부신경', '설하신경', '오십견', '칼슘 채널', '총비골신경',
    // 이번 배치 3차 신규 처방 생성 완료
    '천마구등음', '축천환', '실소산', '금령자산'
]);

const content = fs.readFileSync(srcPath, 'utf8');
const lines = content.split('\n');

const items = [];
const regex = /^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]/;

for (const line of lines) {
    const m = line.match(regex);
    if (m) {
        items.push({ count: parseInt(m[1]), name: m[2] });
    }
}

const remaining = [];
let completedCount = 0;
let completedRefs = 0;

for (const it of items) {
    if (COMPLETED_BATCH_3.has(it.name)) {
        completedCount++;
        completedRefs += it.count;
    } else {
        remaining.append ? remaining.append(it) : remaining.push(it);
    }
}

console.log('Original items:', items.length);
console.log(`Completed in Batch 3: ${completedCount} items (${completedRefs} references resolved)`);
console.log('Remaining items:', remaining.length);

const totalRemainingRefs = remaining.reduce((acc, cur) => acc + cur.count, 0);

const out = [];
out.push('---');
out.push('title: "미노트화 링크 목록 (정제판 v7 - 배치 3차 처방 및 핵심개념 반영)"');
out.push('type: worklist');
out.push('owner: 다빈치');
out.push('updated: 2026-09-04');
out.push('---');
out.push('');
out.push('# 🔗 미노트화 링크 — 생성 대기 개념 후보 (정제판 v7)');
out.push('');
out.push(`> [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** ${remaining.length}종 / ${totalRemainingRefs}회.`);
out.push(`> *(2026-09-04 배치 1·2·3차 누적 완료: 최상위 핵심 개념 77종 / 약 1,620회 참조 해결 반영)*`);
out.push('');
out.push('## 📊 참조 빈도');

for (const r of remaining) {
    const countStr = r.count.toString().padStart(4, ' ');
    out.push(`- \`${countStr}회\` → [[${r.name}]]`);
}

fs.writeFileSync(srcPath, out.join('\n') + '\n', 'utf8');
console.log('Successfully updated:', srcPath);
