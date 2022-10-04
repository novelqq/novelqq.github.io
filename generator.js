const pug = require('pug');
const fs = require('fs');
var apikey = null;
fs.readFile('./env/apikey.txt', (err, data) => {
    if(err) throw err;
    apikey = data;
});










const index = pug.compileFile('./index.pug');
const gallery = pug.compileFile('./gallery.pug');

//create html files
fs.writeFile('index.html', index({}), (err) => {
    if (err) throw err;
});

fs.writeFile('gallery.html', gallery({}), (err) => {
    if (err) throw err;
});
