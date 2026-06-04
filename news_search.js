const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 604800;

const queries = [
  '英超 阿森纳 新闻 2026年5月',
  '英超 曼城 夺冠 新闻 2026年5月',
  '英超 曼联 切尔西 新闻 2026年5月',
  '欧冠 决赛 巴黎 2026年5月',
  '意甲 国米 西甲 新闻 2026年5月'
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:20000, maxBuffer: 1024*1024});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0,3).forEach(doc => {
        console.log(doc.title || '');
        if (doc.passage) console.log(doc.passage.substring(0,600));
        console.log('---');
      });
    } else if (d.msg) {
      console.log('msg: ' + d.msg);
    }
  } catch(e) { console.log('err: '+e.message.substring(0,200)); }
}
