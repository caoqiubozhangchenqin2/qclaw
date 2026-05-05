const https = require('https');

const API_KEY = 'c4906718aabe4287b5963a412e4c81ce';
const BASE = 'api.football-data.org';

// 获取积分榜
function getStandings() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: BASE,
      path: '/v4/competitions/PL/standings',
      headers: { 'X-Auth-Token': API_KEY }
    };
    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

// 获取四队比赛
function getTeamMatches(teamId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: BASE,
      path: `/v4/teams/${teamId}/matches?status=SCHEDULED&limit=5`,
      headers: { 'X-Auth-Token': API_KEY }
    };
    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

async function main() {
  // 积分榜
  const standings = await getStandings();
  const table = standings.standings[0].table;
  console.log('\n=== 英超积分榜 ===');
  table.forEach((t, i) => {
    console.log(`${i+1} ${t.team.name} ${t.points}分｜${t.playedGames}场｜${t.won}/${t.draw}/${t.lost}`);
  });

  // 四队比赛
  const teams = [
    { id: 57, name: '阿森纳' },
    { id: 64, name: '切尔西' },
    { id: 71, name: '桑德兰' },
    { id: 66, name: '曼联' }
  ];

  for (const team of teams) {
    const matches = await getTeamMatches(team.id);
    console.log(`\n=== ${team.name} 近期比赛 ===`);
    matches.matches.forEach(m => {
      const date = new Date(m.utcDate);
      const time = date.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      console.log(`${m.homeTeam.name} vs ${m.awayTeam.name}｜${time}｜${m.competition.name}`);
    });
  }
}

main().catch(console.error);
