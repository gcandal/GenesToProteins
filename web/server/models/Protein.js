module.exports = function(sequelize, DataTypes) {
    return sequelize.define('Protein', {
        proteinID: {
            type: DataTypes.STRING,
            primaryKey: true
        }
    });
};
