app.controller('listProteinsController', [ '$scope', '$http','$location',
	function($scope, $http, $location){
		$http.get('/api/getAllProteins').then(function (result) {
			console.log(result);
			$scope.proteins = [];
			for(var i = 0; i < result['data'].length; i++) {
				var tempObj = {};
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
		});
	}]
);