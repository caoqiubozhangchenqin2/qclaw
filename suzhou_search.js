const {execSync} = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const now = Math.floor(Date.now()/1000);
const from = now - 604800; // 7天内

const queries = [
  '苏州东吴 中甲 2026年5月 比赛 赛程',
  '苏州东吴 足球 最新 2026',
  'okooo 英超 切尔西 桑德兰 赔率 0522',
  'okooo 英超 阿森纳 水晶宫 赔率 0522',
  'okooo 英超 曼联 布莱顿 赔率 0522',
  '天空体育预测 英超 第37轮 比分',
  '英超 阿森纳 曼城 夺冠 2026',
  'wsbk 2026 赛程 第七站 第八站'
];

for (const kw of queries) {
  const p = JSON.stringify({keyword: kw, from_time: from, to_time: now});
  try {
    const r = execSync('node "' + script + '" "' + p.replace(/"/g, '\\"') + '"', {encoding:'utf8', timeout:20000, maxBuffer: 1024*1024});
    const d = JSON.parse(r);
    console.log('\n=== ' + kw + ' ===');
    if (d.success && d.data && d.data.docs) {
      d.data.docs.slice(0,4).forEach(doc => {
        console.log(doc.title || '');
        if (doc.passage) console.log(doc.passage.substring(0,800));
        console.log('---');
      });
    } else if (d.msg) {
      console.log('msg: ' + d.msg);
    }
  } catch(e) { console.log('err: '+e.message.substring(0,200)); }
}
