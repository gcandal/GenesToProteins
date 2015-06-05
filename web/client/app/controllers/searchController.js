app.controller('searchController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		$scope.name = "";
		$scope.searchDone = false;
		$scope.search = function(name) {
			if(name != "" && name != null && name != undefined) {
				$http.get('/api/searchGenes/' + name).then(function (result) {
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
				$http.get('/api/searchProtein/' + name).then(function (result) {
					console.log(result);
					$scope.proteins = [];
					for(var i = 0; i < result['data'].length; i++) {
						var tempObj = {};
						//tempObj['ensembleId'] =
						delete result['data'][i]['TranscriptProtein'];
						delete result['data'][i]['createdAt'];
						delete result['data'][i]['updatedAt'];
						delete result['data'][i]['pdb_url'];
						delete result['data'][i]['protein_names'];
						delete result['data'][i]['uniprot_url'];
						delete result['data'][i]['interactions'];
						delete result['data'][i]['keywords_molecular_function'];
						delete result['data'][i]['keywords_biological_process'];
						delete result['data'][i]['keywords_ligand'];
						delete result['data'][i]['taxonomic_lineage'];

						Object.keys(result['data'][i]).forEach(function (key) {
							tempObj[underscoreToDash(key)] = result['data'][i][key];
						});
						$scope.proteins.push(tempObj);
					}
					//$scope.proteins = result['data'];
					$scope.searchDone = true;
				});
			}
		}
	}]
);