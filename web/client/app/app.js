'use strict';

var app = angular.module("app", ['ngRoute','ngResource'])
	.config(function($routeProvider, $locationProvider) {
	    $routeProvider
				.when('/',
					 {templateUrl: 'app/views/search.html'},
					 {controller: 'controllers/searchController.js'}
					)
				.when('/protein/:proteinId',
					{templateUrl: 'app/views/protein.html'},
					{controller: 'controllers/proteinController.js'}
				)
				.when('/gene/:geneId',
					{templateUrl: 'app/views/gene.html'},
					{controller: 'controllers/geneController.js'}
				).when('/listGenes',
					{templateUrl: 'app/views/listGenes.html'},
					{controller: 'controllers/listGenesController.js'}
				).when('/listProteins',
					{templateUrl: 'app/views/listProteins.html'},
					{controller: 'controllers/listProteinsController.js'}
				).when('/addGene',
					{templateUrl: 'app/views/addGene.html'},
					{controller: 'controllers/addGeneController.js'}
				).when('/getCSV',
					{templateUrl: 'app/views/getCSV.html'},
					{controller: 'controllers/getCSVController.js'}
				)
				.otherwise({redirectTo: '/'});
	});