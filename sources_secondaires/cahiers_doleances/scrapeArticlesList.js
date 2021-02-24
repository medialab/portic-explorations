const dsv = require('d3-dsv');
const fs = require('fs');
const { tmpdir } = require('os');
const { resolve } = require('path');
const sandcrawler = require('sandcrawler')

const listOfLists = dsv.csvParse(fs.readFileSync('data/metalist_with_pagination.csv', 'utf8'));

const parseList = (item) => {
  return new Promise((resolve, reject) => {
    sandcrawler.spider()
    .url(item.url)
    .scraper(function($, done) {
      console.log('parsing', item.url)
      const data = $('.menu_articles li').scrape({
        title: {sel: 'a'},
        url: function($) {
          return `http://www.histoirepassion.eu/${$(this).find('a').attr('href').split('./').pop()}`
        }
      });

      done(null, data);
    })
    .result(function(err, req, res) {
      if(err) return reject(err)
      resolve(res.data.map(datum => {
        const parts = datum.title.match(/([\d]{4}) - ([^(]+) \(([\d]+)\)/);


        return {
          ...item, 
          ...datum, 
          parentTitle: item.title,
          year: parts && parts[1],
          locality: parts && parts[2],
          department: parts && parts[3],
          title_clean: datum.title.split(':').pop().trim()
        }
      }))
    })
    .run(function(err, remains) {
      if(err) return reject(err)
      // console.log('And we are done!');
    });
  })
}

listOfLists
.reduce((cur, list) => {
  console.log('processing', list.url);

  return cur
  .then(temp => new Promise((res, rej) => {
    console.log('parsing', list.url);
    parseList(list)
    .then(results => {
      console.log('got results for', list.url)
      const newResults = [...temp, ...results]
      res(newResults);
    })
    .catch(rej)
  }
  ))

}, Promise.resolve([]))
.then(data => {
  // const flattened = data.reduce((res, datum) => [...res, ...datum], [])
  fs.writeFileSync('data/articles_list.csv', dsv.csvFormat(data) , 'utf8')
  console.log('done');
})