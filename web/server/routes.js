// Load modules

var Gene = require('./controllers/gene'),
    Protein = require('./controllers/protein'),
    Static    = require('./static');



// API Server Endpoints
exports.endpoints = [
  { method: 'GET',  path: '/{somethingss*}', config: Static.get },
  { method: 'GET', path: '/api/searchGenes/{stringG}', config: Gene.search},
  { method: 'GET', path: '/api/searchProtein/{stringP}', config: Protein.search},
  { method: 'GET', path: '/api/gene/{geneId}', config: Gene.getOne},
  { method: 'GET', path: '/api/protein/{userId}', config: Protein.getOne}
];