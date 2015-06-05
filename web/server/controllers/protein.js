'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    sequelize = Models.sequelize,
    Protein = Models.Protein;

exports.search = {
    handler: function (request, reply) {
        Protein.findAll({ where:  ["name like \'%" + request.params.name + "%\'"]}).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound(''));
        });
    }
};

exports.getOne = {
    handler: function (request, reply) {
        Protein.find(request.params.proteinId).then(function (protein) {
            if (protein != null) {
                return reply(protein);
            }
            return reply(Boom.notFound(''));
        });
    }
};

exports.getProteinTranscripts = {
    handler: function (request, reply) {
        Protein.find(request.params.proteinId).then(function (protein) {
            if (protein != null) {
                return reply(protein.getTranscripts());
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
            reply(Boom.notFound(error));
        });
    }
};

exports.getProteinThreePrimes = {
    handler: function (request, reply) {
        sequelize.query("select * from threeprimeprotein where ProteinName = \'" +  request.params.proteinId + "\'", { type: sequelize.QueryTypes.SELECT})
            .then(function(genes) {
                return reply(genes);
            }).catch(function (error) {
                console.log(error);
                reply(Boom.notFound(error));
            });

        /*Gene.find(request.params.geneId).then(function (gene) {
         if (gene != null) {
         return reply(gene.getThreePrimeProteins());
         }
         return reply(Boom.notFound('')); // 500 error
         }).catch(function (error) {
         reply(Boom.notFound(error));
         });*/
    }
};