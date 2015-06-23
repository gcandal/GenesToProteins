app.controller('getCSVController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		var nameG;
		$scope.notifications = [];
		$scope.table = 'Proteins';
		$scope.type = 'csv';
		$scope.name = "";
		$scope.getCSV = function(table, type) {
			console.log(table);
			console.log(type);
			if(table != "" && table != null && table != undefined) {
				$http.get('/api/getCSV/' + table + '/' + type).then(function (result) {
					console.log(result);

					/*if(result['data'] == true) {
						$location.path('/gene/' + nameG);
					} else {
						$scope.notifications.pop();
						$scope.notifications.push("Failed to find a gene with ID " + nameG);
					}*/
				});
			}
		}
	}]
);