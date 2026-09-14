const https = require('https');
const url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=superior+gluteal+nerve+entrapment&retmode=json&retmax=5';

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    const json = JSON.parse(data);
    console.log('PMIDs:', json.esearchresult.idlist);
    // fetch details for first 3
    const ids = json.esearchresult.idlist.slice(0, 3).join(',');
    const sumUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${ids}&retmode=json`;
    https.get(sumUrl, (res2) => {
      let data2 = '';
      res2.on('data', (chunk) => data2 += chunk);
      res2.on('end', () => {
        const sumJson = JSON.parse(data2);
        for (const id of json.esearchresult.idlist.slice(0, 3)) {
          const item = sumJson.result[id];
          console.log(`\nID: ${id}`);
          console.log(`Title: ${item.title}`);
          console.log(`Authors: ${item.authors.map(a => a.name).join(', ')}`);
          console.log(`Source: ${item.source} (${item.pubdate})`);
          console.log(`DOI: ${item.articleids.find(x => x.idtype === 'doi')?.value}`);
        }
      });
    });
  });
});
