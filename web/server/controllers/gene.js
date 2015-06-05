'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    Gene = Models.Gene,
    sequelize = Models.sequelize;


exports.search = {
    handler: function (request, reply) {
        Gene.findAll({ where:  ["ensembleID like \'%" + request.params.geneId + "%\'"]}).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.getOne = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            var methods = [];
            for (var m in gene) {
                if (typeof gene[m] == "function") {
                    methods.push(m);
                }
            }
            //console.log(methods.join("\n"));
            //console.log(gene.getGeneTranscripts);
            //console.log(gene.getThreePrimeProteins);
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
            reply(Boom.notFound(error));
        });
    }
};

exports.getGeneTranscripts = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene.getTranscripts());
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
            reply(Boom.notFound(error));
        });
    }
};

exports.getGeneThreePrimes = {
    handler: function (request, reply) {
        sequelize.query("select * from threeprimeprotein where GeneEnsembleID = \'" +  request.params.geneId + "\'", { type: sequelize.QueryTypes.SELECT})
            .then(function(prots) {
                return reply(prots);
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