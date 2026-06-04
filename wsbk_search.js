const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 259200;

const queries = [
  'wsbk 2026 捷克 莫斯特 第六站 第七站 赛程',
  'wsbk 2026 赛历 schedule 完整',
  '张雪机车 WSBK 德比斯 2026 最新'
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:20000, maxBuffer: 1024*1024});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0,5).forEach(doc => {
        console.log(doc.title || '');
        if (doc.passage) console.log(doc.passage.substring(0,800));
        console.log('---');
      });
    } else if (d.msg) {
      console.log('msg: ' + d.msg);
    }
  } catch(e) { console.log('err: '+e.message.substring(0,200)); }
}
