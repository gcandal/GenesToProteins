app.controller('geneController', [ '$scope', '$http','$location', '$routeParams',
		function($scope, $http, $location, $routeParams) {
			console.log($routeParams.geneId);

			$http.get('/api/gene/' + $routeParams.geneId).then(function(data){
				console.log(data);
				// $scope.sectionList = data;
			}).catch(function(error){
				console.log("error" + error);
			})
	}]
);