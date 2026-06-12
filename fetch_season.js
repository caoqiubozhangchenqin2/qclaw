const https = require('https');
const token = 'c4906718aabe4287b5963a412e4c81ce';
const fetch = (path) => new Promise((res, rej) => {
  const req = https.get({ hostname: 'api.football-data.org', path, headers: { 'X-Auth-Token': token } }, r => {
    let d = '';
    r.on('data', c => d += c);
    r.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(new Error('Parse:' + d)); } });
  });
  req.on('error', rej);
  req.setTimeout(10000, () => { req.destroy(); rej(new Error('Timeout')); });
});
(async () => {
  try {
    const r = await fetch('/v4/competitions/PL/seasons');
    process.stdout.write('SEASONS\n' + JSON.stringify(r) + '\n');
  } catch(e) {
    process.stderr.write('ERR:' + e.message + '\n');
  }
})();