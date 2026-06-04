const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 259200;

const queries = [
  '苏州东吴 中甲 2026年5月 比赛',
  '苏州东吴 足球 赛程 最新 2026',
  '英超 阿森纳 新闻 2026年5月',
  '英超 曼城 新闻 2026年5月',
  '英超 曼联 切尔西 新闻 2026年5月',
  '欧冠 决赛 2026年5月 新闻',
  '意甲 西甲 德甲 新闻 2026年5月',
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:15000});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0,3).forEach(doc => {
        console.log(doc.title || '');
        console.log((doc.passage || '').substring(0,500));
        console.log('---');
      });
    } else { console.log('no data'); }
  } catch(e) { console.log('err: '+e.message.substring(0,200)); }
}
