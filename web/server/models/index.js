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
    m.Gene.belongsToMany(m.Transcript, {through: 'GeneTranscript'});
    m.Transcript.belongsToMany(m.Gene, {through: 'GeneTranscript'});
    m.Transcript.belongsToMany(m.Protein, {through: 'TranscriptProtein'});
    m.Protein.belongsToMany(m.Transcript, {through: 'TranscriptProtein'});
    m.Gene.belongsToMany(m.Protein, {through: 'ThreePrimeProtein', as: 'ThreePrimeProteins'});
    m.Protein.belongsToMany(m.Gene, {through: 'ThreePrimeProtein', as: 'ThreePrimeProteins'});
})(module.exports);

sequelize
//.sync({    force: true})
    .sync()
    .then(syncSuccess, syncError);

var exec = require('child_process').exec;
exec('../../C/bin/transform -both ../../proteinDatabase.db ./csvs', function(error, stdout, stderr) {
    console.log('stdout: ', stdout);
    console.log('stderr: ', stderr);
    if (error !== null) {
        console.log('exec error: ', error);
    }
});

function syncSuccess() {
    console.log('Succesfully synced DB!');
}

function syncError(ex) {
    console.log('Error while executing DB sync: '+ ex.message, 'error');
}

module.exports.sequelize = sequelize;