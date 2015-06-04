app.controller('geneController', [ '$scope', '$http','$location', '$routeParams',
		function($scope, $http, $location, $routeParams) {
			$http.get('/api/gene/' + $routeParams.geneId).then(function(data){
				console.log(data);
				$scope.organism = data['data']['organism'];
				$scope.gene = data['data'];
				delete $scope.gene['organism'];
				delete $scope.gene['createdAt'];
				delete $scope.gene['updatedAt'];
				return $http.get('/api/geneTranscripts/'+ $routeParams.geneId);
				// $scope.sectionList = data;
			}).then(function(result) {
				console.log(result['data']);
				$scope.transcripts = result['data'];
				$scope.proteins = {};
				$scope.transcripts.map(function(transcript) {
					$http.get('/api/transcriptProteins/'+ transcript['transcriptId']).then(function(result) {
						if($scope.proteins[transcript['transcriptId']] == null)
							$scope.proteins[transcript['transcriptId']]= [];
						delete result['data'][0]['TranscriptProtein'];
						delete result['data'][0]['createdAt'];
						delete result['data'][0]['updatedAt'];
						delete result['data'][0]['pdb_url'];
						delete result['data'][0]['uniprot_url'];


						$scope.proteins[transcript['transcriptId']].push(result['data']);
						console.log($scope.proteins);
					});
				});
			}).catch(function(error){
				console.log("error" + error)
			});
	}]
);