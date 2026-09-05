// patch-graph.js
// @quartz-community/graph: 현재 페이지 slug가 location.pathname에서 퍼센트 인코딩된 채로
// 들어와 한글/비ASCII slug 노트에서 그래프가 노드를 못 찾는 버그를 고친다.
// m = Fu(w) → m = Fu(decodeURIComponent(w))
const fs = require("fs");
const path = require("path");

const pkgDir = path.join(
  __dirname,
  "..",
  "node_modules",
  "@quartz-community",
  "graph",
  "dist",
  "components",
);
const file = path.join(pkgDir, "index.js");

try {
  if (!fs.existsSync(file)) {
    console.log("[patch-graph] graph component not found, skipping");
    process.exit(0);
  }
  let s = fs.readFileSync(file, "utf-8");
  const from = "var m=Fu(w)";
  const to = `var m=Fu((function(t){try{return decodeURIComponent(t)}catch(e){return t}})(w))`;
  if (s.includes(to)) {
    console.log("[patch-graph] already patched");
    process.exit(0);
  }
  const count = s.split(from).length - 1;
  if (count !== 1) {
    console.log(`[patch-graph] unexpected matches (${count}), skipping`);
    process.exit(0);
  }
  s = s.replace(from, to);
  fs.writeFileSync(file, s, "utf-8");
  console.log("[patch-graph] patched slug decoding");
} catch (err) {
  console.log("[patch-graph] failed:", err.message);
  process.exit(0);
}
