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
server = Http.createServer(function onRequest(request, response) {
    router( request, response, function( error ) {
        if ( !error ) {
            response.writeHead( 404 );
        } else {
            // Handle errors
            console.log( error.message, error.stack );
            response.writeHead( 400 );
        }
        response.end( '\n' );
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
    let query = request.body;
    //console.log(request);
    console.log('news');
}
router.post('/news/_search', searchNews);

/* Search in facebook collection */
function searchFacebook( request, response){
    let queryString = request.body.query.match.content;
    let responseData = {};
    console.log(request.body);
    console.log('fb');
    fb.haterccu.find({$text:{$search: queryString}}, {score:{$meta:"textScore"}}).sort( { score: { $meta: "textScore" } } ).toArray(function(err, result){
        if (err) console.log('Error');
        console.log(result);
        console.log(result.length);
        responseData.hit = result;
    });
    esponse.writeHead(200, {'Content-Type': 'application/json'});
    response.json(responseData);
    response.end();
}
router.post('/facebook/_search', searchFacebook);
