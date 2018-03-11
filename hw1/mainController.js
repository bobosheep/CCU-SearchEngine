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
    },
    "from": 10
  }

  $scope.searchPages = [{
      "num":1,
      "display": false
    }, {
      "num":2,
      "display": false
    }, {
      "num":3,
      "display": false
    }, {
      "num":4,
      "display": false
    }, {
      "num":5,
      "display": false
    }, {
      "num":6,
      "display": false
    }, {
      "num":7,
      "display": false
    }, {
      "num":8,
      "display": false
    }, {
      "num":9,
      "display": false
    } , {
      "num":10,
      "display": false
  }];

  $scope.searchResult = {
    "searchTime" : '',
    "resultTotal" : ''
  }
  
  $scope.response = ''
  $scope.search = function(val, page){
    $scope.body.query.match.content = val;
    $scope.body.from = (page - 1) * 10;
    let total = 0;
    $scope.response = $http.post($scope.searchHost, $scope.body,{
        headers: {
          'Access-Control-Allow-Origin':'*'
        },  
      }).then(function(response){
        //console.log(response.data);
        $scope.response = response.data;
        total = $scope.response.hits.total;
        $scope.searchResult.resultTotal = 'Total ' + total  + ' results' 
        $scope.searchPages.forEach(function(p, i){
          if((p.num - 1) * 10 < total){
            p.display = true;
            //console.log(p);
          }
          else{
            p.display = false;
          }
        });
        $scope.searchResult.searchTime = 'Search Time : ' + $scope.response.took+ ' ms'
        //$scope.highlightInfo = $scope.response.hits.hits.highlight.content.for;
        return response.data.hits;
      })
      .catch(function (error) {
        console.log(error);
      });
    //console.log(res);
    
  }

}]);