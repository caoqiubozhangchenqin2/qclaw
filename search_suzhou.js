const { execSync } = require('child_process');
const script = 'D:\\Qclaw\\v0.2.24.540\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now() / 1000);
const from = now - 259200;

const queries = [
  '苏州东吴 中甲 2026年6月 比赛',
  '苏州东吴 足球 赛程 6月',
  '苏州东吴 中甲 积分榜'
];

for (const kw of queries) {
  const p = JSON.stringify({ keyword: kw, from_time: from, to_time: now });
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', { encoding: 'utf8', timeout: 15000 });
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0, 4).forEach(doc => {
        console.log(doc.title || '');
        console.log(doc.passage.substring(0, 600));
        console.log('---');
      });
    } else {
      console.log(JSON.stringify(d).substring(0, 300));
    }
  } catch(e) { console.log('err: ' + e.message); }
}