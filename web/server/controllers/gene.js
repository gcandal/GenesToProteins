'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    Gene = Models.Gene;

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

exports.create = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
            reply(Boom.notFound(error));
        });
    }
};

exports.update = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
            reply(Boom.notFound(error));
        });
    }
};

exports.remove = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound('')); // 500 error
        }).catch(function (error) {
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