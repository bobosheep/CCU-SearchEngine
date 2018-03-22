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
  //request url
  $scope.searchHost = {
    "show" : false,
    "all" :'http://localhost:9200/_search',
    "news" : 'http://localhost:9200/news/_search',
    "facebook" :'http://localhost:9200/facebook/_search'
  }
  //query body
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
    "from": 1
  }

  $scope.searchPages = [{
      "url" : '',
      "num":1,
      "display": false
    }, {
      "url" : '',
      "num":2,
      "display": false
    }, {
      "url" : '',
      "num":3,
      "display": false
    }, {
      "url" : '',
      "num":4,
      "display": false
    }, {
      "url" : '',
      "num":5,
      "display": false
    }, {
      "url" : '',
      "num":6,
      "display": false
    }, {
      "url" : '',
      "num":7,
      "display": false
    }, {
      "url" : '',
      "num":8,
      "display": false
    }, {
      "url" : '',
      "num":9,
      "display": false
    } , {
      "url" : '',
      "num":10,
      "display": false
  }];

  $scope.searchResult = {
    "searchTime" : '',
    "resultTotal" : ''
  }
  
  $scope.response = ''

  //search function
  $scope.search = function(url, val, page){
    if(val.length === 0){
      console.log('Empty');
      return;
    }
    $scope.body.query.match.content = val;

    $scope.body.from = (page - 1) * 10;
    let total = 0;

    //post request
    $scope.response = $http.post(url, $scope.body,{
        headers: {
          'Access-Control-Allow-Origin':'*'
        },  
      }).then(function(response){
        ///get response
        $scope.response = response.data;
        ///total result
        total = $scope.response.hits.total;
        $scope.searchResult.resultTotal = 'Total ' + total  + ' results' 
        ///pages show control
        $scope.searchPages.forEach(function(p, i){
          p.url = url
          if((p.num - 1) * 10 < total){
            p.display = true;
          }
          else{
            p.display = false;
          }
        });
        ///search time show
        $scope.searchResult.searchTime = 'Search Time : ' + $scope.response.took+ ' ms';
        
        return response.data.hits;
      })
      .catch(function (error) {
        console.log(error);
      });
    
    $scope.searchHost.show = true;
    window.scrollTo(0, 0);
    //console.log(res);
    
  }

}]);