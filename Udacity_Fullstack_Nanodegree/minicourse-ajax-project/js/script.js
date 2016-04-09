
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");
    // load streetview
    var street = $body.find('#street').val();
    var city = $body.find('#city').val();
    var image = $("<img class='bgimg'>");
    var addres = street + ', ' + city;
    //var src = $("http://maps.googleapis.com/maps/api/streetview?size600x400&location=" );
    $greeting.text("So you would like to se "+ addres + '?');
    image.attr('src','http://maps.googleapis.com/maps/api/streetview?size=800x600&location='+ addres );
    $body.append(image);
    // YOUR CODE GOES HERE!
    // NYTimes Ajax request
    var nyTimes_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'+
            'q=' + city + '&sort=newest&api-key=91a27950d1929425a5baa18e4ad20dfc:12:74743487';
    //var req = $.getJSON(nyTimes_url);
    // alert(req);
    // for (var i in req){
    //     alert(req[i]);
    // }
    // $body.append('<p></p>');
    $.getJSON(nyTimes_url, function(data){
        $nytHeaderElem.text('New York Times Articles About' + city);
        var articles = data.response.docs;
        //alert(articles);
        for (var i=0; i < articles.length; i++){
            var article = articles[i];
            // $nytElem.append('<li class="article">'+ 
            //     '<a href="'+article.web_url'">'+ 
            //     article.headline.main+'<p>'+ article.snippet+ 
            //     '</p>'+ '</li>')
            // $('.article').error(function(){
            //     alert('ERROR Occurs!');
             }
        // jQuery.error(function(){
        //         alert('ERROR Occurs!');
        //         $('#nytimes-header').text('New York Times Articles Fails to load!')
            }).error(function(e){
                 $nytHeaderElem.text('New York Times Articles Fails to load!');
             });


    
    
    //My Implementation
    var wiki_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&explaintext=&titles='+ city+'&format=json'
    $.ajax({ url: wiki_url,
             dataType: "jsonp",
             success : function(data){
                 $.each(data.query.pages, function(i,item) {
                    var title = item.title;
                    //var text = item.extract;
                    $("#wikipedia-links").append('<li><a href="https://en.wikipedia.org/wiki/'+title+'">'+title+'</a></li>');
                    //$("#wikipedia-links").append('<p>'+text+'</p>')
                    //alert(item.title);
                    });    
             }})

    
    //Course implementation
    // var wiki_url2 = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + city + '&format=json&callback=wikiCallback';
    // $.ajax({
    //     url:wiki_url2,
    //     dataType: 'jsonp',
    //     success: function(response){
    //         var articleList = response[1];
    //         for (var i=0; i< articleList.length; i++) {
    //             var articleStr = articleList[i]
    //             var url = 'https://en.wikipedia.org/wiki/' + articleStr;
    //             $wikiElem.append('<li><a href="'+ url+'">'+ articleStr+'</a></li>');
    //         };
    //     }
    // });

    return false;
    };
//if form will be submitted the function runs
$('#form-container').submit(loadData);


// 1600 pennsylvania ave washington dc