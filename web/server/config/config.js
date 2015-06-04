'use strict';

module.exports = {
  server: {
    host: 'localhost',
    port: 8080
  },
  database: {
    dialect: "sqlite",
    storage: "../../proteinDatabase.db",
  	host: 'localhost',
    port: 80,
    db: 'ProteinGenes.db',
    username: '',
    password: ''
  }
};
