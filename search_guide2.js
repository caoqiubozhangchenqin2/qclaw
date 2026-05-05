const { execSync } = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now() / 1000);

const queries = [
  { keyword: '阿森纳 vs 富勒姆 赔率 2026年5月', label: '赔率1' },
  { keyword: '曼联 vs 利物浦 赔率 胜平负 2026', label: '赔率2' },
  { keyword: '狼队 vs 桑德兰 赔率 2026', label: '赔率3' },
  { keyword: '英超第35轮 阿森纳 富勒姆 新闻 2026年5月', label: '新闻1' },
  { keyword: '英超 曼联 利物浦 比赛新闻 2026年5月', label: '新闻2' },
  { keyword: '桑德兰 英超 2026 保级 升级区', label: '新闻3' }
];

let out = '';
queries.forEach(q => {
  try {
    const p = JSON.stringify({ keyword: q.keyword, from_time: now - 172800, to_time: now });
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', { encoding: 'utf8', timeout: 20000 });
    const d = JSON.parse(r);
    out += '\n=== ' + q.label + ' ===\n';
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0, 2).forEach(doc => {
        out += (doc.title || '') + '\n' + (doc.passage || '').substring(0, 400) + '\n---\n';
      });
    } else {
      out += 'no data\n';
    }
  } catch (e) {
    out += 'err: ' + e.message + '\n';
  }
});
console.log(out);
