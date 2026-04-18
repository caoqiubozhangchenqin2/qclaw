const { execSync } = require('child_process');
const script = 'D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs';
const fromTime = Math.floor(Date.now()/1000) - 604800;
const toTime = Math.floor(Date.now()/1000);

const queries = [
  '英超阿森纳伯恩茅斯爆冷',
  '央视五大联赛版权免费',
  'B席离开曼城告别',
  '埃基蒂克跟腱断裂利物浦',
  '欧联四强英超诺丁汉森林'
];

for (const kw of queries) {
  const param = JSON.stringify({ keyword: kw, industry: 'news', from_time: fromTime, to_time: toTime });
  try {
    const result = execSync(`node "${script}" "${param.replace(/"/g, '\\"')}"`, { encoding: 'utf8', timeout: 15000 });
    const parsed = JSON.parse(result);
    console.log(`\n=== ${kw} ===`);
    if (parsed.success && parsed.data && parsed.data.docs) {
      for (const doc of parsed.data.docs.slice(0, 2)) {
        console.log(`TITLE: ${doc.title}`);
        console.log(`SNIPPET: ${doc.passage}`);
        console.log(`DATE: ${doc.date}`);
        console.log(`URL: ${doc.url}`);
        console.log('---');
      }
    } else {
      console.log('No results or failed:', parsed.message);
    }
  } catch (e) {
    console.log(`Error for ${kw}: ${e.message}`);
  }
}
