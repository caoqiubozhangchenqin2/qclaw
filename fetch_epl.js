const https = require('https');
const token = 'c4906718aabe4287b5963a412e4c81ce';

const get = (url) => new Promise((resolve, reject) => {
  https.get(url, {headers:{'X-Auth-Token': token}}, res => {
    let d = '';
    res.on('data', c => d += c);
    res.on('end', () => resolve(JSON.parse(d)));
  }).on('error', reject);
});

async function main() {
  // 英超积分榜
  const standing = await get('https://api.football-data.org/v4/competitions/PL/standings');
  const table = standing.standings.find(s => s.type === 'TOTAL');
  console.log('=== 英超积分榜 ===');
  table.table.slice(0,20).forEach(r => {
    console.log(r.position + '. ' + r.team.name + ' ' + r.points + 'pts ' + r.playedGames + 'G ' + r.won + 'W/' + r.draw + 'D/' + r.lost + 'L');
  });
  console.log('');

  // 四队近期比赛
  const teams = [{id:57,name:'Arsenal'},{id:64,name:'Chelsea'},{id:71,name:'Sunderland'},{id:66,name:'Man Utd'}];
  for (const t of teams) {
    const m = await get('https://api.football-data.org/v4/teams/'+t.id+'/matches?status=SCHEDULED&limit=5');
    const up = m.matches.filter(x=>x.competition.id===2021).slice(0,2);
    if(up.length) {
      console.log('=== ' + t.name + ' upcoming ===');
      up.forEach(mm => {
        const d = new Date(mm.utcDate);
        const local = d.toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'});
        console.log(mm.homeTeam.name + ' vs ' + mm.awayTeam.name + ' | ' + local + ' | ' + (mm.venue||'TBD'));
      });
    }
  }
}
main().catch(console.error);
