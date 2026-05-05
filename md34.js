const https = require('https');

// Get matchday 34 results for tracked teams
const req = https.request('https://api.football-data.org/v4/competitions/PL/matches?matchday=34', {
  headers: { 'X-Auth-Token': 'c4906718aabe4287b5963a412e4c81ce' }
}, res => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const r = JSON.parse(d);
    const tracked = [57, 64, 71, 66];
    r.matches.filter(m => tracked.includes(m.homeTeam.id) || tracked.includes(m.awayTeam.id))
      .forEach(m => {
        const df = new Date(m.utcDate).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
        console.log(m.homeTeam.shortName + ' ' + m.score.fullTime.home + ' : ' + m.score.fullTime.away + ' ' + m.awayTeam.shortName + ' | ' + df + ' | ' + m.status);
      });
  });
});
req.end();
