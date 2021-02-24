const dsv = require('d3-dsv');
const fs = require('fs');
const { tmpdir } = require('os');
const { resolve } = require('path');
const sandcrawler = require('sandcrawler')

const list = dsv.csvParse(fs.readFileSync('data/articles_list.csv', 'utf8'));

const COOLING_TIME = 2000;

const parseArticle = (item) => {
  return new Promise((resolve, reject) => {
    sandcrawler.spider()
    .url(item.url)
    .scraper(function($, done) {
      console.log('parsing', item.url)
      const data = $('#content').scrape({
        chapo_html: function($) {
          return $(this).find('.chapo.surlignable').html()
        },
        chapo_txt: function($) {
          return $(this).find('.chapo.surlignable').text()
        },
        texte_cahier_html: function($) {
          return $(this).find('.texte').html()
        },
        texte_cahier_txt: function($) {
          return $(this).find('.texte').text()
        },
        
      });

      done(null, data);
    })
    .timeout(20000)
    .result(function(err, req, res) {
      if(err) {
        // console.log('retrying')
        // getting just what we can get
        resolve({
          ...item,
          // ...res.data[0]
        })
      }
      resolve({
        ...item,
        ...res.data[0]
      })
    })
    .run(function(err, remains) {
      if(err) return reject(err)
      // console.log('And we are done!');
    });
  })
}

list
.reduce((cur, article, index) => {

  return cur
  .then(temp => new Promise((res, rej) => {
    setTimeout(() => {
      console.log('processing', index + 1 + '/' + list.length, article.url);
      parseArticle(article)
      .then(results => {
        console.log('got results for', article.url)
        const newResults = [...temp, results]
        res(newResults);
      })
      .catch(rej)
    }, COOLING_TIME)
    
  }
  ))

}, Promise.resolve([]))
.then(data => {
  fs.writeFileSync('data/articles_list.csv', dsv.csvFormat(data) , 'utf8')
  console.log('done');
})
.catch(console.log)