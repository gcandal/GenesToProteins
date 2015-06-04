'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    Transcript = Models.Transcript;

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
        Transcript.find(request.params.transcriptId).then(function (transcript) {
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

exports.getTranscriptProteins = {
    handler: function (request, reply) {
        Transcript.find(request.params.transcriptId).then(function (transcript) {
            var methods = [];
            for (var m in transcript) {
                if (typeof transcript[m] == "function") {
                    methods.push(m);
                }
            }
            //console.log(methods.join("\n"));
            //console.log(transcript.getProteins());

            return reply(transcript.getProteins());

        }).catch(function (error) {
            console.log(error);
            reply(Boom.notFound(error));
        });
    }
};

/*exports.removeAll = {
    validate: {
        payload: {
            geneId: Joi.string().required(),
        }
    },
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};*/