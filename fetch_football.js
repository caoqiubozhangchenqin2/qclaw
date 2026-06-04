const https = require('https');
const apiKey = 'c4906718aabe4287b5963a412e4c81ce';

function apiGet(path) {
  return new Promise((resolve, reject) => {
    const url = new URL('https://api.football-data.org/v4' + path);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'GET',
      headers: { 'X-Auth-Token': apiKey }
    };
    let data = '';
    const req = https.request(options, res => {
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { reject(new Error('JSON parse failed: ' + data.substring(0,200))); }
      });
    });
    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

async function main() {
  // 1. 获取英超积分榜
  const standings = await apiGet('/competitions/PL/standings');
  const table = standings.standings.find(s => s.type === 'TOTAL');
  console.log('=== STANDINGS ===');
  table.table.forEach(r => {
    console.log(`${r.position}. ${r.team.shortName} - ${r.points}pts ${r.playedGames}场 ${r.won}/${r.draw}/${r.lost}`);
  });
  console.log('Matchday:', standings.season.currentMatchday);

  // 2. 获取四队近期比赛（未来7天内的）
  const teamIds = [57, 64, 71, 66];
  const now = new Date();
  const weekLater = new Date(now.getTime() + 7 * 86400000);

  for (const tid of teamIds) {
    const teamName = {57:'阿森纳',64:'切尔西',71:'桑德兰',66:'曼联'}[tid];
    const matches = await apiGet(`/teams/${tid}/matches?status=SCHEDULED&limit=10`);
    console.log('\n=== MATCHES ' + teamName + ' ===');
    (matches.matches || []).forEach(m => {
      const md = new Date(m.utcDate);
      if (md >= now && md <= weekLater) {
        const dateStr = (md.getMonth()+1) + '月' + md.getDate() + '日(' + '日一二三四五六'.charAt(md.getDay()) + ') ' +
                        String(md.getHours()).padStart(2,'0') + ':' + String(md.getMinutes()).padStart(2,'0');
        const home = m.homeTeam.shortName;
        const away = m.awayTeam.shortName;
        const comp = m.competition.name;
        console.log(`${home} vs ${away} | ${dateStr} | ${m.venue || 'TBD'} | ${comp}`);
      }
    });
  }
}

main().catch(e => console.error('ERROR:', e.message));