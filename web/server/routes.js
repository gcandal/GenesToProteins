// Load modules

var models = require('./models'),
    Static    = require('./static');

// API Server Endpoints
exports.endpoints = [

  { method: 'GET',  path: '/{somethingss*}', config: Static.get }
  //{ method: 'POST', path: '/user', config: Static.get},
  //{ method: 'GET', path: '/user', config: Static.get},
  //{ method: 'GET', path: '/user/{userId}', config: Static.get},
  //{ method: 'PUT', path: '/user/{userId}', config: Static.get},
  //{ method: 'DELETE', path: '/user/{userId}', config: Static.get},
  //{ method: 'DELETE', path: '/user', config: Static.get}
];