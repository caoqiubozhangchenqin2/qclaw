const https = require('https');
const token = 'c4906718aabe4287b5963a412e4c81ce';
const opts = (path) => ({
  hostname: 'api.football-data.org', path, headers: {'X-Auth-Token': token}
});
const fetch = (p) => new Promise((res, rej) => {
  const req = https.get(opts(p), r => {
    let d = '';
    r.on('data', c => d += c);
    r.on('end', () => {
      try { res(JSON.parse(d)); }
      catch(e) { rej(new Error('Parse error: ' + d)); }
    });
  });
  req.on('error', rej);
  req.setTimeout(15000, () => { req.destroy(); rej(new Error('Timeout')); });
});
(async () => {
  try {
    const [standings, arsMatches, cheMatches, sunMatches, munMatches] = await Promise.all([
      fetch('/v4/competitions/PL/standings'),
      fetch('/v4/teams/57/matches?status=SCHEDULED&limit=10'),
      fetch('/v4/teams/64/matches?status=SCHEDULED&limit=10'),
      fetch('/v4/teams/71/matches?status=SCHEDULED&limit=10'),
      fetch('/v4/teams/66/matches?status=SCHEDULED&limit=10'),
    ]);
    console.log('STANDINGS_OK');
    console.log(JSON.stringify(standings));
    console.log('ARS_MATCHES');
    console.log(JSON.stringify(arsMatches));
    console.log('CHE_MATCHES');
    console.log(JSON.stringify(cheMatches));
    console.log('SUN_MATCHES');
    console.log(JSON.stringify(sunMatches));
    console.log('MUN_MATCHES');
    console.log(JSON.stringify(munMatches));
  } catch(e) {
    console.error('ERROR: ' + e.message);
  }
})();