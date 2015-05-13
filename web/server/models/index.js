var Sequelize = require('sequelize'),
    config = require('../config/config');

var sequelize = new Sequelize(config.database.db, config.database.username, config.database.password, {
    host: config.database.host,
    dialect: config.database.dialect,
    storage: config.database.storage
});

var models = [
    'Gene',
    'Protein',
    'Transcript'
];
models.forEach(function(model) {
    module.exports[model] = sequelize.import(__dirname + '/' + model);
});

(function(m) {
    m.Transcript.belongsToMany(m.Gene, {through: 'GeneTranscript'});
    m.Gene.hasMany(m.Transcript, {through: 'GeneTranscript'});
    m.Transcript.hasMany(m.Protein, {through: 'TranscriptProtein'});
    m.Protein.belongsToMany(m.Transcript, {through: 'TranscriptProtein'});
    m.Gene.hasMany(m.Protein, {through: 'ThreePrimeProtein'});
    m.Protein.belongsToMany(m.Gene, {through: 'ThreePrimeProtein'});
})(module.exports);

sequelize
//.sync({    force: true})
    .sync()
    .then(syncSuccess, syncError);

function syncSuccess() {
    console.log('Succesfully synced DB!');
}

function syncError(ex) {
    console.log('Error while executing DB sync: '+ ex.message, 'error');
}

module.exports.sequelize = sequelize;