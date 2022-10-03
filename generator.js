const pug = require('pug');
const fs = require('fs');

const index = pug.compileFile('./index.pug');

const data = index({});

fs.writeFile('index.html', data, (err) => {
    if (err) throw err;
});
