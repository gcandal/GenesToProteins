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
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.create = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.update = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.remove = {
    handler: function (request, reply) {
        Gene.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
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