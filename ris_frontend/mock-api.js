var express = require('express');
var apiMocker = require('connect-api-mocker');
const port = 3000;
var app = express();
 
app.use('/api', apiMocker('mock-api'));
 
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
