const { execSync } = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const fromTime = Math.floor(Date.now()/1000) - 604800;
const toTime = Math.floor(Date.now()/1000);

const queries = [
  '阿森纳1-2伯恩茅斯 英超第32轮',
  '央视获得英超转播版权 2026',
  '贝尔纳多席尔瓦 曼城 离队',
  '埃基蒂克 跟腱断裂 伤缺9个月',
  '诺丁汉森林 欧联杯 半决赛'
];

for (const kw of queries) {
  const param = JSON.stringify({ keyword: kw, from_time: fromTime, to_time: toTime });
  try {
    const result = execSync(`node "${script}" "${param.replace(/"/g, '\\"')}"`, { encoding: 'utf8', timeout: 15000 });
    const parsed = JSON.parse(result);
    console.log(`\n=== ${kw} ===`);
    if (parsed.success && parsed.data && parsed.data.docs) {
      for (const doc of parsed.data.docs.slice(0, 3)) {
        console.log(`TITLE: ${doc.title}`);
        console.log(`SNIPPET: ${doc.passage}`);
        console.log(`DATE: ${doc.date}`);
        console.log('---');
      }
    } else {
      console.log('No results or failed:', parsed.message);
    }
  } catch (e) {
    console.log(`Error for ${kw}: ${e.message}`);
  }
}
