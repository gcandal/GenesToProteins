app.controller('proteinController', [ '$scope', '$http','$location','$routeParams',
		function($scope, $http, $location, $routeParams) {

			$http.get('/api/proteinThreePrimes/' + $routeParams.proteinId).then(function(data) {
				$scope.threePrimeGenes = data['data'];
				console.log($scope.threePrimeGenes);
			});

			$http.get('/api/protein/' + $routeParams.proteinId).then(function(result){
				//console.log(result);
				$scope.name = result['data']['name'];

				delete result['data']['TranscriptProtein'];
				delete result['data']['createdAt'];
				delete result['data']['updatedAt'];
				delete result['data']['pdb_url'];
				delete result['data']['uniprot_url'];
				delete result['data']['name'];
				$scope.protein = {};
				Object.keys(result['data']).forEach(function (key) {
					$scope.protein[underscoreToDash(key)] = result['data'][key];
				});
				return $http.get('/api/proteinTranscripts/'+ $routeParams.proteinId);
			}).then(function(result) {
				//console.log(result);
				$scope.transcripts = result['data'];
				$scope.genes = {};
				$scope.transcripts.map(function(transcript) {
					$http.get('/api/transcriptGenes/'+ transcript['transcriptId']).then(function(result) {
						//console.log(result);
						for(var i = 0; i < result['data'].length; i++) {
							if($scope.genes[transcript['transcriptId']] == null)
								$scope.genes[transcript['transcriptId']]= [];

							var tempObj = {};
							//tempObj['ensembleId'] =
							delete result['data'][i]['createdAt'];
							delete result['data'][i]['GeneTranscript'];
							delete result['data'][i]['updatedAt'];

							Object.keys(result['data'][i]).forEach(function (key) {
								tempObj[camelToDash(key)] = result['data'][i][key];
							});
							//console.log(tempObj);
							$scope.genes[transcript['transcriptId']].push(tempObj);
						}
					});
				});
			}).catch(function(error){
				console.log("error" + error)
		});
	}]
);

function camelToDash(str) {
	var str2 = str.replace(/\W+/g, ' ').replace(/([a-z\d])([A-Z])/g, '$1 $2');
	return str2.charAt(0).toUpperCase() + str2.slice(1);
}

function underscoreToDash(str){
	var str2 = str.replace(/(\_[a-z])/g, function($1){return $1.toUpperCase().replace('_',' ');});
	return str2.charAt(0).toUpperCase() + str2.slice(1);
}
