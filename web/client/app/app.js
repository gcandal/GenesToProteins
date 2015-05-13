'use strict';

var app = angular.module("app", ['ngRoute','ngResource'])
	.config(function($routeProvider, $locationProvider) {
		//$locationProvider.html5Mode(true);
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
				)
				.otherwise({redirectTo: '/'});
	});