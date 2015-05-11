'use strict';

module.exports = function(sequelize, DataTypes) {
    return sequelize.define('Gene', {
        ensembleID: {
            type: DataTypes.STRING,
            primaryKey: true
        },
        species: {
            type: DataTypes.STRING
        },

        threePrime: {
            type: DataTypes.STRING
        }
    });
};
