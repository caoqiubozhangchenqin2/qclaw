const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 259200;

const queries = [
  '苏州东吴 中甲 2026年5月 比赛',
  '苏州东吴 中甲 最新赛程',
  'okooo 英超 阿森纳 伯恩利 赔率',
  'okooo 英超 埃弗顿 桑德兰 赔率',
  'okooo 英超 曼联 诺丁汉森林 赔率',
  '英超 阿森纳 新闻 2026年5月',
  '英超 曼城 新闻 2026年5月',
  '英超 切尔西 新闻 2026年5月',
  '欧冠 新闻 2026年5月',
  '意甲 西甲 德甲 新闻 2026年5月'
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:20000});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0,3).forEach(doc => {
        console.log(doc.title || '');
        console.log(doc.passage.substring(0,800));
        console.log('---');
      });
    } else {
      console.log(JSON.stringify(d).substring(0,300));
    }
  } catch(e) { console.log('err: '+e.message); }
}