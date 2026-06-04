const {execSync} = require('child_process');
const script = 'C:\\Users\\Administrator\\.qclaw\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 604800;

const queries = [
  '苏州东吴 中甲 2026年5月 比赛 赛程',
  '苏州东吴 足球 最新 2026',
  'okooo 英超 桑德兰 切尔西 赔率 0524',
  'okooo 英超 阿森纳 水晶宫 赔率',
  '天空体育预测 英超 第37轮 比分',
  '英超 阿森纳 夺冠 2026年5月 新闻',
  '英超 曼联 布莱顿 2026年5月 新闻',
  '欧冠 决赛 巴黎 阿森纳 2026年5月',
  '意甲 西甲 德甲 新闻 2026年5月',
  'wsbk 2026 赛程 第六站 第七站 张雪'
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:20000, maxBuffer: 2*1024*1024});
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
  } catch(e) { console.log('err: '+e.message.substring(0,300)); }
}
