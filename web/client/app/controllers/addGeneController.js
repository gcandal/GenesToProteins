app.controller('addGeneController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		var nameG;
		$scope.notifications = [];
		$scope.name = "";
		$scope.searchDone = false;
		console.log($location.path());
		$scope.addGene = function(name) {
			nameG = name;
			if(name != "" && name != null && name != undefined) {
				$http.get('/api/addGene/' + name).then(function (result) {
					if(result['data'] == true) {
						$location.path('/gene/' + nameG);
					} else {
						$scope.notifications.pop();
						$scope.notifications.push("Failed to find a gene with ID " + nameG);
					}
				});
			}
		}
	}]
);