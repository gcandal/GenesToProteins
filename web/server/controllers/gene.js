'use strict';

var Joi = require('joi'),
    Boom = require('boom'),
    Models = require('../models/'),
    Gene = Models.Gene,
    sequelize = Models.sequelize,
    Sequelize = require('sequelize'),
    PythonShell = require('python-shell');


exports.search = {
    handler: function (request, reply) {
        Gene.findAll({ where:  ["ensembleID like \'%" + request.params.name + "%\' OR organism like \'%" + request.params.name + "%\'"]}).then(function (gene) {
            if (gene != null) {
                return reply(gene);
            }
            return reply(Boom.notFound(''));
        }).catch(function (error) {
            reply(Boom.notFound(error));
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

exports.getAll = {
    handler: function (request, reply) {
        Gene.findAll().then(function (gene) {
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

exports.addGene = {
    handler: function (request, reply) {
        var options = {
            mode: 'text',
            pythonPath: '/usr/bin/python2.7',
            scriptPath: '../../',
            args: [request.params.geneId]
        };

        PythonShell.run('scraping.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            if(results[0] == '0')
                reply(true);
            else
                reply(false);
            console.log('results: %j', results);
        });
        /*var python = child.spawn('python', __dirname + "../../scraping.py", request.params.geneId);
        var output = "";
        python.stdout.on('data', function() {
            output += data
        });
        python.on('close', function(code){
            /*if (code !== 0) {
                reply(Boom.notFound());
            }
            reply(output);
        });*/
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

exports.getCSV = {
    handler: function (request, reply) {
        var options = {
            mode: 'text',
            pythonPath: '/usr/bin/python2.7',
            scriptPath: '../../',
            args: [request.params.geneId]
        };

        PythonShell.run('scraping.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            if(results[0] == '0')
                reply(true);
            else
                reply(false);
            console.log('results: %j', results);
        });

        var exec = require('child_process').exec;
        exec('../../C/bin/transform -both ../../proteinDatabase.db ./csvs', function(error, stdout, stderr) {
            console.log('stdout: ', stdout);
            console.log('stderr: ', stderr);
            if (error !== null) {
                console.log('exec error: ', error);
            }
        });

        /*var python = child.spawn('python', __dirname + "../../scraping.py", request.params.geneId);
         var output = "";
         python.stdout.on('data', function() {
         output += data
         });
         python.on('close', function(code){
         /*if (code !== 0) {
         reply(Boom.notFound());
         }
         reply(output);
         });*/
    }
};