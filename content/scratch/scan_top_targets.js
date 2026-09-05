const fs = require('fs');
const path = require('path');

const vaultDir = 'c:/Simbio';
const allNotes = new Map();
const aliasMap = new Map();

function walk(dir) {
    for (const f of fs.readdirSync(dir)) {
        if (f.startsWith('.') || ['node_modules', '30_Sprint_Logs', 'scratch'].includes(f)) continue;
        const p = path.join(dir, f);
        try {
            const st = fs.statSync(p);
            if (st.isDirectory()) walk(p);
            else if (f.endsWith('.md')) {
                const name = f.replace(/\.md$/, '');
                allNotes.set(name.toLowerCase(), { name, path: p });

                // check frontmatter aliases
                try {
                    const content = fs.readFileSync(p, 'utf8');
                    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
                    if (fmMatch) {
                        const aliasMatch = fmMatch[1].match(/aliases:\s*(\[[^\]]*\]|.+)/);
                        if (aliasMatch) {
                            let raw = aliasMatch[1].trim();
                            if (raw.startsWith('[') && raw.endsWith(']')) {
                                raw.slice(1, -1).split(',').forEach(a => {
                                    const cleaned = a.trim().replace(/^["']|["']$/g, '');
                                    if (cleaned) aliasMap.set(cleaned.toLowerCase(), { target: name, path: p });
                                });
                            } else {
                                raw.split(',').forEach(a => {
                                    const cleaned = a.trim().replace(/^["']|["']$/g, '');
                                    if (cleaned) aliasMap.set(cleaned.toLowerCase(), { target: name, path: p });
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
        } catch(e) {}
    }
}
walk(vaultDir);

const worklist = fs.readFileSync('c:/Simbio/_AI_OS/30_Sprint_Logs/미노트화_링크_목록.md', 'utf8');
const lines = worklist.split('\n');
const targets = [];
const regex = /^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]/;

for (const line of lines) {
    const m = line.match(regex);
    if (m) {
        targets.push({ count: parseInt(m[1]), name: m[2] });
    }
}

const alreadyExists = [];
const aliasExists = [];
const partialMatches = [];
const missing = [];

for (const t of targets) {
    const lower = t.name.toLowerCase();
    if (allNotes.has(lower)) {
        alreadyExists.push({ ...t, path: allNotes.get(lower).path });
    } else if (aliasMap.has(lower)) {
        aliasExists.push({ ...t, target: aliasMap.get(lower).target, path: aliasMap.get(lower).path });
    } else {
        let found = [];
        for (const [k, v] of allNotes.entries()) {
            if (k.includes(lower) || lower.includes(k)) {
                found.push(v.name);
            }
        }
        if (found.length > 0) {
            partialMatches.push({ ...t, related: found.slice(0, 3) });
        } else {
            missing.push(t);
        }
    }
}

console.log('=== Total Targets:', targets.length);
console.log('Already Exists (File exists):', alreadyExists.length, 'items');
console.log('Alias Exists:', aliasExists.length, 'items');
console.log('Partial Matches (Possible aliases):', partialMatches.length, 'items');
console.log('Pure Missing:', missing.length, 'items');

console.log('\n--- Top 15 Already Exists (Can be purged from worklist immediately) ---');
alreadyExists.slice(0, 15).forEach(x => console.log(`- ${x.count}회: [[${x.name}]] -> ${path.relative(vaultDir, x.path)}`));

console.log('\n--- Top 15 Partial Matches (Review for Alias Linkage) ---');
partialMatches.slice(0, 15).forEach(x => console.log(`- ${x.count}회: [[${x.name}]] -> related: ${x.related.join(', ')}`));

console.log('\n--- Top 15 Pure Missing (Creation Candidates) ---');
missing.slice(0, 15).forEach(x => console.log(`- ${x.count}회: [[${x.name}]]`));
