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
        },
        taxonomic_lineage: {
            type: DataTypes.STRING,
        },
        organism: {
            type: DataTypes.STRING,
        },
        protein_names: {
            type: DataTypes.STRING,
        },
        taxonomic_identifier: {
            type: DataTypes.STRING,
        },
        proteomes: {
            type: DataTypes.STRING,
        },
        interactions: {
            type: DataTypes.STRING,
        }
        ,
        keywords_molecular_function: {
            type: DataTypes.STRING,
        }
        ,
        keywords_ligand: {
            type: DataTypes.STRING,
        }
        ,
        keywords_biological_process: {
            type: DataTypes.STRING,
        }
    });
};