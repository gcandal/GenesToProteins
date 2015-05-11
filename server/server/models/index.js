var Sequelize = require('sequelize'),
    config = require('../config/config');

// initialize database connection
var sequelize = new Sequelize('proteinDatabase', 'username', 'password', {
    host: 'localhost',
    dialect: config.database.dialect,

    // SQLite only
    storage: './proteinDatabase.db'
});


// load models
var models = [
    'Gene',
    'Protein',
    'Transcript'
];
models.forEach(function(model) {
    module.exports[model] = sequelize.import(__dirname + '/' + model);
});

// describe relationships
(function(m) {
    m.Transcript.belongsToMany(m.Gene, {through: 'GeneTranscript'});
    m.Gene.hasMany(m.Transcript, {through: 'GeneTranscript'});
    m.Transcript.hasMany(m.Protein, {through: 'TranscriptProtein'});
    m.Protein.belongsToMany(m.Transcript, {through: 'TranscriptProtein'});
    m.Gene.hasMany(m.Protein, {through: 'ThreePrimeProtein'});
    m.Protein.belongsToMany(m.Gene, {through: 'ThreePrimeProtein'});
})(module.exports);

sequelize
    .sync()
    .then(syncSuccess, syncError);

function syncSuccess() {
    console.log('Succesfully synced DB!');
}

function syncError(ex) {
    console.log('Error while executing DB sync: '+ ex.message, 'error');
}

// export connection
module.exports.sequelize = sequelize;