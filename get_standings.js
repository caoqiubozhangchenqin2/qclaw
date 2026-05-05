const https = require('https');
const options = {
  hostname: 'api.football-data.org',
  path: '/v4/competitions/PL/standings',
  headers: { 'X-Auth-Token': 'c4906718aabe4287b5963a412e4c81ce' }
};
https.get(options, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const j = JSON.parse(data);
    const t = j.standings[0].table;
    t.forEach((x, i) => console.log(`${i+1} ${x.team.name} ${x.points}分｜${x.playedGames}场｜${x.won}/${x.draw}/${x.lost}`));
  });
});
