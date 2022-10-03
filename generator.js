const pug = require('pug');
const fs = require('fs');

const index = pug.compileFile('./index.pug');
const gallery = pug.compileFile('./gallery.pug');
const data = index({});

fs.writeFile('index.html', data, (err) => {
    if (err) throw err;
});

fs.writeFile('gallery.html', gallery({}), (err) => {
    if (err) throw err;
});
