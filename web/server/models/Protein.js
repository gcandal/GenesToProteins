module.exports = function(sequelize, DataTypes) {
    return sequelize.define('Protein', {
        name: {
            type: DataTypes.STRING,
            primaryKey: true
        },
        uniprot_url: {
            type: DataTypes.STRING,
        },
        pdb_url: {
            type: DataTypes.STRING,
        }
    });
};