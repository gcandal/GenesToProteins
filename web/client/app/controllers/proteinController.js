app.controller('proteinController', [ '$scope', '$http','$location','$routeParams',
		function($scope, $http, $location, $routeParams){

		$http.get('/api/protein/' + $routeParams.proteinId).then(function(data){
			console.log(data);
			// $scope.sectionList = data;
		}).catch(function(error){
			console.log("error" + error);
		})
	}]
);