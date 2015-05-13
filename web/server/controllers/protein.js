'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    Protein = Models.protein;

exports.search = {
    handler: function (request, reply) {
        Protein.findAll({ where:  ["proteinID like \'%" + request.params.geneId + "%\'"]}).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.getOne = {
    handler: function (request, reply) {
        Protein.find(request.params.geneId).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.badImplementation()); // 500 error
        });
    }
};

exports.create = {
    validate: {
        payload: {
            userId   : Joi.string().required(),
            username  : Joi.string().required()
        }
    },
    handler: function (request, reply) {
        var user = new User(request.payload);
        user.save(function (err, user) {
            if (!err) {
                return reply(user).created('/user/' + user._id); // HTTP 201
            }
            if (11000 === err.code || 11001 === err.code) {
                return reply(Boom.forbidden("please provide another user id, it already exist"));
            }
            return reply(Boom.forbidden(err)); // HTTP 403
        });
    }
};

exports.update = {
    validate: {
        payload: {
            username  : Joi.string().required()
        }
    },
    handler: function (request, reply) {
        User.findOne({ 'userId': request.params.userId }, function (err, user) {
            if (!err) {
                user.username = request.payload.username;
                user.save(function (err, user) {
                    if (!err) {
                        return reply(user); // HTTP 201
                    }
                    if (11000 === err.code || 11001 === err.code) {
                        return reply(Boom.forbidden("please provide another user id, it already exist"));
                    }
                    return reply(Boom.forbidden(err)); // HTTP 403
                });
            }
            else{
                return reply(Boom.badImplementation(err)); // 500 error
            }
        });
    }
};

exports.remove = {
    handler: function (request, reply) {
        User.findOne({ 'userId': request.params.userId }, function (err, user) {
            if (!err && user) {
                user.remove();
                return reply({ message: "User deleted successfully"});
            }
            if (!err) {
                return reply(Boom.notFound());
            }
            return reply(Boom.badRequest("Could not delete user"));
        });
    }
};

exports.removeAll = {
    handler: function (request, reply) {
        mongoose.connection.db.dropCollection('users', function (err, result) {
            if (!err) {
                return reply({ message: "User database successfully deleted"});
            }
            return reply(Boom.badRequest("Could not delete user"));
        });
    }
};