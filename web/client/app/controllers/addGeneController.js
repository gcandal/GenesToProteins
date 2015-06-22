app.controller('addGeneController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		$scope.name = "";
		$scope.searchDone = false;
		$scope.addGene = function(name) {
			console.log("asd");
			if(name != "" && name != null && name != undefined) {
				$http.get('/api/addGene/' + name).then(function (result) {
					console.log(result);
				});
			}
		}
	}]
);