const Http = require('http');
const Path = require('path');
const Url = require('url');
const Router = require( 'router' )
const Mongojs = require('mongojs');
const BodyParser = require( 'body-parser' );

router = new Router();
let fbURL = "facebook";
let newsURL = "news";
let dbURL = "mydb"
let fbcollections = ["haterccu"];
let newscollections = ["ettoday"];
let mydbCollections = ["news", "facebook"];
let fb = Mongojs(fbURL, fbcollections);
let news = Mongojs(newsURL, newscollections);
let all = Mongojs(dbURL, mydbCollections);

/* Create Server with port 3300 */
server = Http.createServer(function (request, response) {
    router( request, response, function( error ) {
        if ( !error ) {
            response.writeHead( 200 );
        } else {
            // Handle errors
            console.log( error.message, error.stack );
            response.writeHead( 400 );
        }
        response.end( '123' );
    });
    
    
}).listen(3300, function() {
    console.log( 'Listening on port 3300' );
});
router.use( BodyParser.json() );


/* Search in two collection in mongodb */
function searchAll( request, response){
    let queryString = request.body.query.match.content;
    console.log(request.body);
    let startTime = new Date().getTime();
    let res1 = [];
    let res2 = [];
    let result = [];
    res1 = all.news.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).toArray(function(err, fresult){
        res1 = fresult == null ? [] : fresult; 
        all.facebook.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).toArray(function(err, ffresult){
            res2 = ffresult == null ? [] : ffresult;
           // console.log(res1[0]);
            //console.log(res2[0]);
            let endTime = new Date().getTime();
            result = res1.concat(res2).sort(function(a, b){
                if(a.score > b.score)   return -1;
                else if (a.score < b.score) return 1;
                else return 0;
            });
            
            let costTime = endTime - startTime;
            console.log(costTime + "ms" );
        
            let pfrom = request.body.from;
            let end = pfrom + request.body.size; 
            //console.log(pfrom, end);
            let responseData = {
                hits: {
                    hits: []
                }
            };
            for(let i = 0 ; i < (result == null ? 0 : result.length); i++){
                if (i === 0 || i === result.length - 1) {
                    console.log(result[i].score);
                }
                result[i] = {
                    "_id": result[i]._id,
                    "_collection": "ettoday",
                    "_score": result[i].score,
                    "_source":{
                        "content" : result[i].content,
                        "created_time" : result[i].create_time,
                        "id" : result[i].id,
                        "title" : result[i].title,
                        "url" : result[i].url
                    },
                    "highlight":{
                        "content":[result[i].content.split("\n")]
                    }
                }
            }
            //console.log(result);
            responseData.hits.total = result == null ? 0 : result.length;
            responseData.hits.hits = result == null ? [] : result.slice(pfrom, end);
            responseData.took = costTime;
            response.writeHead(200, {'Content-Type': 'application/json'});
            responseData = JSON.stringify(responseData);
            response.end(responseData);
        });
    });
   
   
    console.log('ALL');
}
router.post('/_search', searchAll);

/* Search in news collection */
function searchNews( request, response){
    let queryString = request.body.query.match.content;
    console.log(request.body);
    let startTime = new Date().getTime();
    all.news.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).toArray(function(err, result){
        if (err) {
            console.log('Error');
            
        }
        let endTime = new Date().getTime();
        let costTime = endTime - startTime;
        console.log(costTime + "ms" );

        result = result.sort(function(a, b){
            if(a.score > b.score)   return -1;
            else if (a.score < b.score) return 1;
            else return 0;
        });
        //console.log(result);
        let pfrom = request.body.from;
        let end = pfrom + request.body.size; 
        //console.log(pfrom, end);
        let responseData = {
            hits: {
                hits: []
            }
        };
        for(let i = 0 ; i < (result == null ? 0 : result.length); i++){
            result[i] = {
                "_id": result[i]._id,
                "_collection": "ettoday",
                "_score": result[i].score,
                "_source":{
                    "content" : result[i].content,
                    "created_time" : result[i].create_time,
                    "id" : result[i].id,
                    "title" : result[i].title,
                    "url" : result[i].url
                },
                "highlight":{
                    "content":[result[i].content.split("\n")]
                }
            }
        }
        //console.log(result);
        responseData.hits.total = result == null ? 0 : result.length;
        responseData.hits.hits = result == null ? [] : result.slice(pfrom, end);
        responseData.took = costTime;
        response.writeHead(200, {'Content-Type': 'application/json'});
        responseData = JSON.stringify(responseData);
        response.end(responseData);
    });
    console.log('news');
}
router.post('/news/_search', searchNews);

/* Search in facebook collection */
function searchFacebook( request, response){
    let queryString = request.body.query.match.content;
    let searchTime;
    //console.log(request.body);
    fb.haterccu.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).explain("executionStats", function(err, result){
        
        console.log(result);
        searchTime = result.executionStats.executionTimeMillis;
        console.log('321');
    });
    console.log('fb');
    let startTime = new Date().getTime();
    all.facebook.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).toArray(function(err, result){
        if (err) console.log('Error');
        //console.log(result);
        
        let endTime = new Date().getTime();
        let costTime = endTime - startTime;
        console.log(costTime + "ms" );

        result = result.sort(function(a, b){
            if(a.score > b.score)   return -1;
            else if (a.score < b.score) return 1;
            else return 0;
        });
        //console.log(result);
        let pfrom = request.body.from;
        let end = pfrom + request.body.size; 
        //console.log(pfrom, end);
        let responseData = {
            hits: {
                hits: []
            }
        };
        for(let i = 0 ; i < (result == null ? 0 : result.length) ; i++){
            result[i] = {
                "_id": result[i]._id,
                "_collection": "haterccu",
                "_score": result[i].score,
                "_source":{
                    "content" : result[i].content,
                    "id" : result[i].id,
                    "title" : result[i].title,
                    "url" : result[i].url
                },
                "highlight":{
                    "content":[result[i].content]
                }
            }
        }
        //console.log(result);
        responseData.hits.total = result == null ? 0 : result.length;
        responseData.hits.hits = result == null ? [] : result.slice(pfrom, end);
        responseData.took = costTime;
        response.writeHead(200, {'Content-Type': 'application/json'});
        responseData = JSON.stringify(responseData);
        response.end(responseData);
    });
    
}
router.post('/facebook/_search', searchFacebook);
