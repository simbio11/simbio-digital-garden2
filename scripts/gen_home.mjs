#!/usr/bin/env node
/**
 * gen_home.mjs — Simbio Cortex 홈(index.md) 동적 영역 생성기
 *
 *  content/ 를 스캔해서 index.md 안의 마커 구간을 다시 씀:
 *   <!-- SC:STATS:START -->  ... 현황도(총 문서 / 백링크 / 이번 달 / 태그)
 *   <!-- SC:GRID:START -->   ... 저장소 몰아보기 카드(+폴더/파일/태그 수 data 속성)
 *   <!-- SC:RECENT:START --> ... 최근 생성된 노트 목록
 *
 *  의존성 없음(순수 Node). sync_obsidian.py 에서 커밋 직전에 호출됨.
 */
import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const CONTENT = path.join(ROOT, "content")
const INDEX = path.join(CONTENT, "index.md")

// ── 저장소 카드 정의 (폴더명 → 표시) ────────────────────────────────
const CARDS = [
  { dir: "0. 기본의학 공부", href: "0.-기본의학-공부/00_기본의학_MOC", icon: "🩺", color: "var(--cat-exam)", name: "기본의학", desc: "레드플래그 · 응급 감별 · 소화기 · 신경계" },
  { dir: "1. 근골격계 공부", href: "1.-근골격계-공부/00_근골격계_MOC", icon: "🦴", color: "var(--cat-muscle)", name: "근골격계", desc: "근육 · 골격 · 신경 · 이학적 검사 · 추나" },
  { dir: "2. 약리 공부", href: "2.-약리-공부/00_약리_공부_MOC", icon: "🌿", color: "var(--cat-herb)", name: "약리 공부", desc: "본초 · 처방 · 약리성분 · 약침" },
  { dir: "3. 이론 공부", href: "3.-이론-공부/00_이론_공부_MOC", icon: "🧠", color: "var(--cat-theory)", name: "이론 공부", desc: "경락 · 생리 · 질환 · 영양학" },
  { dir: "보고서", href: "보고서/주식-브리핑", icon: "📊", color: "var(--cat-formula)", name: "라이프 보고서", desc: "주식 · 부동산 브리핑 · 일상 리서치" },
  { dir: "5. 독서, 노트", href: "5.-독서,-노트/00_독서_노트_moc", icon: "📚", color: "var(--cat-books)", name: "독서·노트", desc: "강의록 · 논문 리뷰 · 독서 노트 · 여행" },
]

const RECENT_LIMIT = 8

// ── 파일 수집 ────────────────────────────────────────────────────
function walk(dir) {
  const out = []
  let entries
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true })
  } catch {
    return out
  }
  for (const e of entries) {
    if (e.name.startsWith(".") || e.name.startsWith("_")) continue
    const full = path.join(dir, e.name)
    if (e.isDirectory()) out.push(...walk(full))
    else if (e.isFile() && e.name.toLowerCase().endsWith(".md")) out.push(full)
  }
  return out
}

function countDirs(dir) {
  let n = 0
  let entries
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true })
  } catch {
    return 0
  }
  for (const e of entries) {
    if (e.isDirectory() && !e.name.startsWith(".") && !e.name.startsWith("_")) {
      n += 1 + countDirs(path.join(dir, e.name))
    }
  }
  return n
}

// ── 프론트매터 / 태그 / 날짜 파싱 ─────────────────────────────────
function parseFront(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  return m ? m[1] : ""
}

function extractTags(raw) {
  const tags = new Set()
  const fm = parseFront(raw)
  // frontmatter: inline  tags: [a, b]  또는  블록 리스트
  const inline = fm.match(/^tags:\s*\[([^\]]*)\]/m)
  if (inline) {
    inline[1].split(",").map((s) => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean).forEach((t) => tags.add(t))
  } else {
    const block = fm.match(/^tags:\s*\r?\n((?:\s*-\s*.+\r?\n?)+)/m)
    if (block) {
      block[1].split(/\r?\n/).map((l) => l.replace(/^\s*-\s*/, "").trim().replace(/^["']|["']$/g, "")).filter(Boolean).forEach((t) => tags.add(t))
    }
  }
  return tags
}

function countBacklinks(raw) {
  const body = raw.replace(/```[\s\S]*?```/g, "")
  const m = body.match(/(^|[^!])\[\[[^\]]+\]\]/gm)
  return m ? m.length : 0
}

const isMOC = (base) => /(^00_|_MOC$|_moc$|MOC$)/.test(base) || /템플릿|template/i.test(base)

/**
 * 명시적 "생성일"만 인정한다.
 *  - 파일명 앞 YYYY-MM-DD (데일리/일자 노트)
 *  - 프론트매터 created / date / 생성일 / 작성일
 * (repo git 이력은 볼트 일괄 이전분이라 신뢰 불가 → 사용 안 함)
 * 명시 날짜가 없으면 null.
 */
function explicitDate(file, raw) {
  const base = path.basename(file)
  const fn = base.match(/(20\d{2})[-_.](\d{2})[-_.](\d{2})/)
  if (fn) return new Date(`${fn[1]}-${fn[2]}-${fn[3]}T00:00:00`)
  const fm = parseFront(raw)
  const fd = fm.match(/^(?:created|date|생성일|작성일)\s*:\s*["']?(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})/m)
  if (fd) return new Date(`${fd[1]}-${String(fd[2]).padStart(2, "0")}-${String(fd[3]).padStart(2, "0")}T00:00:00`)
  return null
}

function titleOf(file, raw) {
  const fm = parseFront(raw)
  const t = fm.match(/^title\s*:\s*["']?(.+?)["']?\s*$/m)
  if (t) return t[1].trim()
  return path
    .basename(file, ".md")
    .replace(/^20\d{2}[-_.]\d{2}[-_.]\d{2}[-_ ]*/, "")
    .replace(/_/g, " ")
    .trim()
}

// ── 스캔 ────────────────────────────────────────────────────────
const allFiles = walk(CONTENT).filter((f) => path.basename(f).toLowerCase() !== "index.md")

const now = new Date()
const curYM = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`

let totalBacklinks = 0
const allTags = new Set()
let thisMonth = 0
const recents = []

for (const f of allFiles) {
  let raw = ""
  try {
    raw = fs.readFileSync(f, "utf8")
  } catch {
    continue
  }
  totalBacklinks += countBacklinks(raw)
  for (const t of extractTags(raw)) allTags.add(t)
  const cd = explicitDate(f, raw)
  if (cd) {
    const ym = `${cd.getFullYear()}-${String(cd.getMonth() + 1).padStart(2, "0")}`
    if (ym === curYM) thisMonth++
  }
  const base = path.basename(f, ".md")
  if (cd && !isMOC(base)) recents.push({ file: f, date: cd, title: titleOf(f, raw), base })
}

recents.sort((a, b) => b.date - a.date)

// 폴더별 카운트
function folderStats(dirName) {
  const dir = path.join(CONTENT, dirName)
  const files = walk(dir)
  const tags = new Set()
  for (const f of files) {
    try {
      for (const t of extractTags(fs.readFileSync(f, "utf8"))) tags.add(t)
    } catch {}
  }
  return { files: files.length, folders: countDirs(dir), tags: tags.size }
}

// ── 블록 생성 ───────────────────────────────────────────────────
const fmtNum = (n) => n.toLocaleString("en-US")

const statsBlock = `<div class="sc-stats">
<div class="sc-stat"><span class="sc-stat-k">총 문서</span><span class="sc-stat-v">${fmtNum(allFiles.length)}</span></div>
<div class="sc-stat"><span class="sc-stat-k">백링크</span><span class="sc-stat-v sc-stat-green">${fmtNum(totalBacklinks)}</span></div>
<div class="sc-stat"><span class="sc-stat-k">이번 달</span><span class="sc-stat-v sc-stat-amber">+${fmtNum(thisMonth)}</span></div>
<div class="sc-stat"><span class="sc-stat-k">태그</span><span class="sc-stat-v sc-stat-blue">${fmtNum(allTags.size)}</span></div>
</div>`

const gridBlock =
  `<div class="sc-grid">\n` +
  CARDS.map((c) => {
    const s = folderStats(c.dir)
    return `<a class="sc-card" href="${c.href}" style="--c:${c.color}" data-files="${s.files}" data-folders="${s.folders}" data-tags="${s.tags}"><span class="sc-ico">${c.icon}</span><span class="sc-txt"><span class="sc-name">${c.name}</span><span class="sc-sub"><span class="sc-desc">${c.desc}</span><span class="sc-count">📄 ${s.files} · 📁 ${s.folders} · 🏷️ ${s.tags}</span></span></span><span class="sc-go">→</span></a>`
  }).join("\n") +
  `\n</div>`

const recentBlock =
  `<div class="sc-recent">\n\n` +
  recents
    .slice(0, RECENT_LIMIT)
    .map((r) => {
      const d = `${r.date.getFullYear()}-${String(r.date.getMonth() + 1).padStart(2, "0")}-${String(r.date.getDate()).padStart(2, "0")}`
      const disp = r.title.replace(/\|/g, "·").replace(/\[/g, "(").replace(/\]/g, ")").trim()
      return `- [[${r.base}|${disp}]]<span class="sc-recent-d">${d}</span>`
    })
    .join("\n") +
  `\n\n</div>`

// ── index.md 갱신 ──────────────────────────────────────────────
function replaceRegion(text, key, block) {
  const s = `<!-- SC:${key}:START -->`
  const e = `<!-- SC:${key}:END -->`
  const re = new RegExp(`${s}[\\s\\S]*?${e}`)
  if (!re.test(text)) {
    console.warn(`[gen_home] marker ${key} not found — skipped`)
    return text
  }
  return text.replace(re, `${s}\n${block}\n${e}`)
}

let idx = fs.readFileSync(INDEX, "utf8")
idx = replaceRegion(idx, "STATS", statsBlock)
idx = replaceRegion(idx, "GRID", gridBlock)
idx = replaceRegion(idx, "RECENT", recentBlock)
fs.writeFileSync(INDEX, idx)

console.log(
  `[gen_home] 문서 ${allFiles.length} · 백링크 ${totalBacklinks} · 이번달 +${thisMonth} · 태그 ${allTags.size} · 최근 ${Math.min(RECENT_LIMIT, recents.length)}건 반영`,
)
