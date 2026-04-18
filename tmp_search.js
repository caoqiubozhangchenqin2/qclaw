const { execSync } = require('child_process');
const ft = Math.floor(Date.now()/1000) - 604800;
const tt = Math.floor(Date.now()/1000);

const searches = [
  { keyword: '中甲苏州东吴2026年4月赛程', from_time: ft, to_time: tt },
  { keyword: '五大联赛热门新闻', from_time: ft, to_time: tt },
  { keyword: '苏超苏州队2026赛程', from_time: ft, to_time: tt }
];

for (const s of searches) {
  const arg = JSON.stringify(s);
  try {
    const out = execSync(`node "D:\\Qclaw\\resources\\openclaw\\config\\skills\\online-search\\scripts\\prosearch.cjs" "${arg.replace(/"/g, '\\"')}"`, { encoding: 'utf8' });
    console.log('=== ' + s.keyword + ' ===');
    console.log(out);
  } catch(e) {
    console.log('=== ' + s.keyword + ' === ERROR');
    console.log(e.message);
  }
}
