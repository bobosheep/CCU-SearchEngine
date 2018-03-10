var app = angular.module('myApp', []);
app.config(function($sceProvider) {
  // Completely disable SCE.  For demonstration purposes only!
  // Do not use in new projects or libraries.
  $sceProvider.enabled(false);
});
app.controller('mainController', ['$scope','$http', '$sce', function($scope, $http, $sce){
  $scope.searchtext = {
    "content":""
  }
  $scope.searchHost = 'http://localhost:9200/_search';

  $scope.body = {
    "query":{
      "match" :{
        "content":  ""
      }    
    },
    "highlight": {
      "pre_tags" : ["<span class='highlight'>"],
      "post_tags" : ["</span>"],
      "fields" : {
          "content" : {}
      }
    }
  }
  console.log($scope.query);

  $scope.highlightInfo = '';
  $scope.searchResult = {
    "searchTime" : '',
    "resultTotal" : ''
  }
  
  $scope.response = ''
  $scope.search = function(val){
    $scope.body.query.match.content = val;
    console.log($scope.query);
    let res = $http.post($scope.searchHost, $scope.body,{
      headers: {
        'Access-Control-Allow-Origin':'*'
      },  
  }).then(function(response){
        console.log(response.data);
        $scope.response = response.data;
        $scope.searchResult.resultTotal = 'Approximately ' + $scope.response.hits.total  + ' results' 
      
        $scope.searchResult.searchTime = 'Search Time : ' + $scope.response.took+ ' ms'
        //$scope.highlightInfo = $scope.response.hits.hits.highlight.content.for;
        return response.data;
      })
      .catch(function (error) {
      console.log(error);
      });
    console.log(res);
    ///$scope.$apply();
  }
}]);