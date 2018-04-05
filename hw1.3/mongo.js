const Http = require('http');
const Path = require('path');
const Url = require('url');
const Router = require( 'router' )
const Mongojs = require('mongojs');
const BodyParser = require( 'body-parser' );

router = new Router();
let fbURL = "facebook";
let newsURL = "news" 
let fbcollections = ["haterccu"];
let newscollections = ["ettoday"];
let fb = Mongojs(fbURL, fbcollections);
let news = Mongojs(newsURL, newscollections);

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
    /*
       let urlParts = Url.parse(request.url);
       //console.log(urlParts);
       let fullPath = urlParts.pathname;
       //console.log(fullPath);
       let jsonUserOject = '';
       if (fullPath == "/facebook/_search") {
            console.log('Yes');
            let responseData = {};
            request.on('data', function(chunk) {
                jsonUserObject = JSON.parse(chunk.toString());
                console.log(jsonUserOject);
                //let queryString = jsonUserOject.query.match.content;
                fb.haterccu.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).toArray(function(err, result){
                    if (err) console.log('Error');
                    console.log(result);
                    responseData = result;
                });
                
                
            });
            //response.writeHead(200, {'Content-Type': 'application/json'});
            //response.json(responseData);
            response.end();
       }
       else {
            response.writeHead(200, {'Content-Type': 'text/html'});
            response.write(request.url);
            response.end();
       }
       */
    
}).listen(3300, function() {
    console.log( 'Listening on port 3300' );
});
router.use( BodyParser.json() );


/* Search in two collection in mongodb */
function searchAll( request, response){
    let query = request.body;
    //console.log(request.body);
    console.log('ALL');
}
router.post('/_search', searchAll);

/* Search in news collection */
function searchNews( request, response){
    let queryString = request.body.query.match.content;
    console.log(request.body);
    news.ettoday.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).sort( { score: { $meta: "textScore" } } ).toArray(function(err, result){
        if (err) {
            console.log('Error');
            
        }
        //console.log(result);
        let pfrom = request.body.from;
        let end = pfrom + request.body.size; 
        //console.log(pfrom, end);
        let responseData = {
            hits: {
                hits: []
            }
        };
        for(let i = 0 ; i < (result.length == null ? 0 : result.length); i++){
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
                    "content":[result[i].content.split("，")]
                }
            }
        }
        //console.log(result);
        responseData.hits.totals = result.length;
        responseData.hits.hits = result.slice(pfrom, end);
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
    
    console.log(request.body);
    //console.log('fb');
    fb.haterccu.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).sort( { score: { $meta: "textScore" } } ).toArray(function(err, result){
        if (err) console.log('Error');
        //console.log(result);
        let pfrom = request.body.from;
        let end = pfrom + request.body.size; 
        //console.log(pfrom, end);
        let responseData = {
            hits: {
                hits: []
            }
        };
        for(let i = 0 ; i < result.length ; i++){
            result[i] = {
                "_id": result[i]._id,
                "_collection": "haterccu",
                "_score": result[i].score,
                "_source":{
                    "content" : result[i].content,
                    "created_time" : result[i].create_time,
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
        responseData.hits.totals = result.length;
        responseData.hits.hits = result.slice(pfrom, end);
        response.writeHead(200, {'Content-Type': 'application/json'});
        responseData = JSON.stringify(responseData);
        response.end(responseData);
    });
    
}
router.post('/facebook/_search', searchFacebook);
