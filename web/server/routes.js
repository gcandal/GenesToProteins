// Load modules

var models = require('./models'),
    Static    = require('./static');



// API Server Endpoints
exports.endpoints = [

  { method: 'GET',  path: '/{somethingss*}', config: Static.get },
  { method: 'GET', path: 'api/searchGenes/{string}', config: models.Gene.find()},
  { method: 'GET', path: 'api/searchProtein/{string}', config: Static.get},
  { method: 'GET', path: 'api/gene/{geneId}', config: models.Gene.find(geneId)},
  { method: 'GET', path: 'api/protein/{userId}', config: Static.get}
];