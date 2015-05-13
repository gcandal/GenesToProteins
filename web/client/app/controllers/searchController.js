app.controller('searchController', [ '$scope', '$http','$location',
		function($scope, $http, $location){

		$scope.uploadfile = function(){
			$http.post('/upload',$scope.file).then(function(data){
				console.log('success');
				// $scope.sectionList = data;
			}).catch(function(error){
				console.log("error" + error);
			})
		};

		$scope.onFileSelect = function($files){
			$scope.file = $files[0].name; 
			console.log($scope.file);
		}
	}]
);