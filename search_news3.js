const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 172800;

const queries = [
  ['苏州东吴 榆林矿工旅投 2026年5月16日 中甲', 3],
  ['阿森纳 伯恩利 赔率 胜平负 威廉希尔 5月', 3],
  ['埃弗顿 桑德兰 赔率 胜平负 威廉希尔', 3],
  ['曼联 诺丁汉森林 赔率 胜平负 威廉希尔', 3],
  ['英超 桑德兰 保级 形势 2026年5月', 3],
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
        console.log(doc.passage.substring(0, 1200));
        console.log('---');
      });
    } else {
      console.log(JSON.stringify(d).substring(0,500));
    }
  } catch(e) { console.log('err: '+e.message); }
}