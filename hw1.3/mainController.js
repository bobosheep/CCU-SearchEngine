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
  //search kernel
  $scope.searchKernel = {
    "options":[{
      "name":"ElasticSearch",
      "url":"http://localhost:9200"
    },{
      "name":"MongoDB",
      "url":"http://localhost:3300"
    },{
      "name":"Solr"
    }],
    "selected":{
      "name":"ElasticSearch",
      "url":"http://localhost:9200"
    }
  }

  //request url
  $scope.searchHost = {
    "show" : false,
    "all" :'/_search',
    "news" : '/news/_search',
    "facebook" :'/facebook/_search'
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
  $scope.nowpage = 1;
  $scope.total = 0;
  //search function
  $scope.search = function(url, val, page){
    if(val.length === 0){
      console.log('Empty');
      return;
    }
    
    url = $scope.searchKernel.selected.url + url;
    
    $scope.body.query.match.content = val;


    if((page - 1) * 10 > $scope.total){
      page = page - 1;
    } else if(page > 10){
      page = 10;
    } else if(page < 1){
      page = 1;
    }
    $scope.nowpage = page;
    $scope.body.from = (page - 1) * 10;
    

    //post request
    $scope.response = $http.post(url, $scope.body,{
        headers: {
          'Access-Control-Allow-Origin':'*'
        },  
      }).then(function(response){
        ///get response
        $scope.response = response.data;
        ///total result
        $scope.total = $scope.response.hits.total;
        $scope.searchResult.resultTotal = 'Total ' + $scope.total  + ' results' 
        ///pages show control
        $scope.searchPages.forEach(function(p, i){
          p.url = url
          if((p.num - 1) * 10 < $scope.total){
            p.display = true;
          }
          else{
            p.display = false;
          }
        });
        ///search time show
        $scope.searchResult.searchTime = 'Search Time : ' + $scope.response.took+ ' ms';
        
        console.log(url);
        console.log($scope.searchHost);
        if(url == $scope.searchKernel.selected.url + $scope.searchHost.all){
          $('#all').addClass("is-active");
          $('#news').removeClass("is-active");
          $('#facebook').removeClass("is-active");
        } else if(url == $scope.searchKernel.selected.url + $scope.searchHost.news){
          $('#all').removeClass("is-active");
          $('#news').addClass("is-active");
          $('#facebook').removeClass("is-active");
        } else if(url == $scope.searchKernel.selected.url + $scope.searchHost.facebook){
          $('#all').removeClass("is-active");
          $('#news').removeClass("is-active");
          $('#facebook').addClass("is-active");
        }
        for(let i = 1 ; i <= 10 ; i++){
              if(page == i){
                $("#" + i).addClass("is-current");
              }
              else{
                $("#" + i).removeClass("is-current");
              }
            }
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