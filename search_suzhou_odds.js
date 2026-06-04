const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 259200;

const queries = [
  ['苏州东吴 中甲 2026年5月 比赛', 3],
  ['okooo 英超 阿森纳 伯恩利 赔率', 3],
  ['okooo 英超 埃弗顿 桑德兰 赔率', 3],
  ['okooo 英超 曼联 诺丁汉森林 赔率', 3],
];

for (const [kw, limit] of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:25000});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0, limit).forEach(doc => {
        console.log(doc.title || '');
        console.log(doc.passage.substring(0, 1000));
        console.log('---');
      });
    } else {
      console.log(JSON.stringify(d).substring(0,500));
    }
  } catch(e) { console.log('err: '+e.message); }
}