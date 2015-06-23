// Load modules

var Gene = require('./controllers/gene'),
    Protein = require('./controllers/protein'),
    Transcript = require('./controllers/transcript'),
    Static    = require('./static');



// API Server Endpoints
exports.endpoints = [
    { method: 'GET',  path: '/{somethingss*}', config: Static.get },
    { method: 'GET', path: '/api/searchGenes/{name}', config: Gene.search},
    { method: 'GET', path: '/api/searchProtein/{name}', config: Protein.search},
    { method: 'GET', path: '/api/gene/{geneId}', config: Gene.getOne},
    { method: 'GET', path: '/api/getAllGenes', config: Gene.getAll},
    { method: 'GET', path: '/api/transcript/{transcriptId}', config: Transcript.getOne},
    { method: 'GET', path: '/api/transcriptProteins/{transcriptId}', config: Transcript.getTranscriptProteins},
    { method: 'GET', path: '/api/transcriptGenes/{transcriptId}', config: Transcript.getTranscriptGenes},
    { method: 'GET', path: '/api/geneTranscripts/{geneId}', config: Gene.getGeneTranscripts},
    { method: 'GET', path: '/api/geneThreePrimeProteins/{geneId}', config: Gene.getGeneThreePrimes},
    { method: 'GET', path: '/api/protein/{proteinId}', config: Protein.getOne},
    { method: 'GET', path: '/api/getAllProteins', config: Protein.getAll},
    { method: 'GET', path: '/api/proteinThreePrimes/{proteinId}', config: Protein.getProteinThreePrimes},
    { method: 'GET', path: '/api/proteinTranscripts/{proteinId}', config: Protein.getProteinTranscripts},
    { method: 'GET', path: '/api/addGene/{geneId}', config: Gene.addGene},
    { method: 'GET', path: '/api/getCSV/{table}/{type}', config: Gene.getCSV}
];