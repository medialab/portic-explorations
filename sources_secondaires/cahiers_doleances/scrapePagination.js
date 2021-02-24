const dsv = require('d3-dsv');
const fs = require('fs');
const sandcrawler = require('sandcrawler')

const listOfLists = dsv.csvParse(fs.readFileSync('data/metalist.csv', 'utf8'));

const parsePagination = ({url, title}) => {
  return new Promise((resolve, reject) => {
    sandcrawler.spider()
    .url(url)
    .scraper(function($, done) {
      console.log('parsing', url)
      var data = $('.pagination a').scrape({
        title: {sel: 'a'},
        url: function($) {
          return `http://www.histoirepassion.eu/${$(this).attr('href').split('./').pop()}`
        }
      });

      done(null, data);
    })
    .result(function(err, req, res) {
      const {data} = res;
      if(err) return reject(err)
      if (data.length) {
        resolve([
          {url, title, page: 0},
          ...data.map(({url}, page) => ({url, title, page: page + 1}))
        ])
      }
      resolve([{url, title, page: 0}])
    })
    .run(function(err, remains) {
      if(err) return reject(err)
      // console.log('And we are done!');
    });
  })
  
}

const storeListsWithPagination = () => {
  Promise.all(listOfLists.map(parsePagination))
  .then(data => {
    const flattened = data.reduce((res, arr) => [...res, ...arr], []);
    fs.writeFileSync('data/metalist_with_pagination.csv', dsv.csvFormat(flattened) , 'utf8')
    console.log('done');
  })
}



storeListsWithPagination();