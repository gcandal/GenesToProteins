app.controller('geneController', [ '$scope', '$http','$location', '$routeParams',
		function($scope, $http, $location, $routeParams) {
			$http.get('/api/geneThreePrimeProteins/' + $routeParams.geneId).then(function(data) {
				$scope.threePrimeProteins = data['data'];
				console.log($scope.threePrimeProteins);
			});


			$http.get('/api/gene/' + $routeParams.geneId).then(function(data){
				//console.log(data);
				$scope.organism = data['data']['organism'];
				delete data['data']['organism'];
				delete data['data']['createdAt'];
				delete data['data']['updatedAt'];
				$scope.gene = {};
				Object.keys(data['data']).forEach(function (key) {
					$scope.gene[camelToDash(key)] = data['data'][key];
				});
				//$scope.gene = data['data'];
				return $http.get('/api/geneTranscripts/'+ $routeParams.geneId);
				// $scope.sectionList = data;
			}).then(function(result) {
				//console.log(result['data']);
				$scope.transcripts = result['data'];
				$scope.proteins = {};
				$scope.transcripts.map(function(transcript) {
					$http.get('/api/transcriptProteins/'+ transcript['transcriptId']).then(function(result) {
						console.log(result);
						for(var i = 0; i < result['data'].length; i++) {
							if($scope.proteins[transcript['transcriptId']] == null)
								$scope.proteins[transcript['transcriptId']]= [];

							var tempObj = {};
							//tempObj['ensembleId'] =
							delete result['data'][i]['TranscriptProtein'];
							delete result['data'][i]['createdAt'];
							delete result['data'][i]['updatedAt'];
							delete result['data'][i]['pdb_url'];
							delete result['data'][i]['uniprot_url'];

							Object.keys(result['data'][i]).forEach(function (key) {
								tempObj[underscoreToDash(key)] = result['data'][i][key];
							});
							$scope.proteins[transcript['transcriptId']].push(tempObj);
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
