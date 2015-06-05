app.controller('listGenesController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		$http.get('/api/getAllGenes').then(function (result) {
			$scope.genes = [];
			for(var i = 0; i < result['data'].length; i++) {
				delete result['data'][i]['createdAt'];
				delete result['data'][i]['updatedAt'];
				var tempObj = {};

				Object.keys(result['data'][i]).forEach(function (key) {
					tempObj[camelToDash(key)] = result['data'][i][key];
				});
				$scope.genes.push(tempObj);
			}
			//$scope.genes = result['data'];
			$scope.searchDone = true;
		});
	}]
);