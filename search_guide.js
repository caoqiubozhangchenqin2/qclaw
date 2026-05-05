const { execSync } = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now() / 1000);

const queries = [
  { keyword: '中甲联赛 苏州东吴 2026年5月 赛程', label: '中甲苏州东吴' },
  { keyword: '英超 第35轮 阿森纳 富勒姆 赔率 2026', label: '阿森纳vs富勒姆赔率' },
  { keyword: '英超 赔率 曼联vs利物浦 威廉希尔 2026', label: '曼联vs利物浦赔率' },
  { keyword: '英超第35轮 比赛结果 2026年5月', label: '第35轮赛果' }
];

let out = '';
queries.forEach(q => {
  try {
    const p = JSON.stringify({ keyword: q.keyword, from_time: now - 172800, to_time: now });
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', { encoding: 'utf8', timeout: 20000 });
    const d = JSON.parse(r);
    out += '\n=== ' + q.label + ' ===\n';
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0, 3).forEach(doc => {
        out += (doc.title || '') + '\n' + (doc.passage || '').substring(0, 400) + '\n---\n';
      });
    } else {
      out += 'no data\n' + (r.substring(0, 200)) + '\n';
    }
  } catch (e) {
    out += 'err: ' + e.message + '\n';
  }
});
console.log(out);
