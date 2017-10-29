





$(document).ready(function() {
	loadMPDatabase("../../../data/government/mp_list.xml");
	loadVotingRecord();
	initTwitter();
	initFacebookFeed();


});



function loadMPDatabase(filelocation) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            var docXML = xhttp.responseXML;
            console.log("got MP list XML")
    	}
  	};
  	xhttp.open("GET", filelocation, true);
  	xhttp.send();
}






//*******************************************************************************************
//
//		VOTING RECORD MODULE
//
//*******************************************************************************************




class PieChart {

	constructor(data, containerselector) {
		this.data = data;
		this.elementId = containerselector;
		// this.canvas = d3.select(containerselector);
	}

	initChart() {
		var containerEl = document.getElementById( this.elementId ),
	        width       = containerEl.clientWidth,
	        height      = width,
	        radius      = Math.min( width, height ) / 2,
	        container   = d3.select( containerEl ),
	        svg         = container.append( 'svg' )
	        					  .attr("id", "pieChartSVG")
	                              .attr( 'width', width )
	                              .attr( 'height', height );
	    var pie = svg.append( 'g' )
	                .attr(
	                  'transform',
	                  'translate(' + width / 2 + ',' + height / 2 + ')'
	                );

	    var detailedInfo = svg.append( 'g' )
	                          .attr( 'class', 'pieChart--detailedInformation' );

	    var twoPi   = 2 * Math.PI;
	    var pieData = d3.pie()
	                    .value( function( d ) { return d.value; } );


	    var arc = d3.arc()
	                    .outerRadius( radius - 10)
	                    .innerRadius( radius - 60 );

	    var pieChartPieces = pie.datum( this.data )
	                            .selectAll( 'path' )
	                            .data( pieData )
	                            .enter()
	                            .append( 'path' )
	                            .attr( 'class', function( d ) {
	                              return 'pieChart__' + d.data.color;
	                            } )
	                            .attr( 'd', arc )
	                            .each( function() {
	                              this._current = { startAngle: 0, endAngle: 0 };
	                            } )
	                            .transition()
	                            .duration( 600 )
	                            .attrTween( 'd', function( d ) {
	                              var interpolate = d3.interpolate( this._current, d );
	                              this._current = interpolate( 0 );
	                              console.log(this._current)

	                              return function( t ) {
	                                return arc( interpolate( t ) );
	                              };
	                            } )
	                            // .each( 'end', function handleAnimationEnd( d ) {
	                            //   // drawDetailedInformation( d.data, this );
	                            // } );
	}

	eraseChart() {

	}

	resetChart() {

	}
}







function loadVotingRecord() {
	var piedata = [
      {
        color       : 'green',
        description : 'Member voted in favour of motion or bill.',
        title       : 'Yea',
        value       : 0.62
      },
      {
        color       : 'blue',
        description : 'Member voted in opposition to motion or bill.',
        title       : 'Nay',
        value       : 0.28
      },
      {
        color       : 'gray',
        description : 'Member was absent, abstained, or was paired for vote.',
        title       : 'None',
        value       : 0.1
      }
    ]
    var votingmodule = d3.select("#main-container").append("div").classed("module-container", true).attr("id", "voting-record");
	votingmodule.append("h2").text("Voting Record Module");
	var pie = new PieChart(piedata, "voting-record");
	pie.initChart();
}









//*******************************************************************************************
//
//		TWITTER MODULE
//
//*******************************************************************************************


function initTwitter() {
	window.twttr = (function(d, s, id) {
			var js, fjs = d.getElementsByTagName(s)[0],
				t = window.twttr || {};
			if (d.getElementById(id)) return t;
			js = d.createElement(s);
			js.id = id;
			js.src = "https://platform.twitter.com/widgets.js";
			fjs.parentNode.insertBefore(js, fjs);

			t._e = [];
			t.ready = function(f) {
				t._e.push(f);
			};

			return t;
		}(document, "script", "twitter-wjs"));
	twttr.ready(function(twttr) {
		loadTwitterFeed("https://twitter.com/JustinTrudeau");
	});
}



function loadTwitterFeed(address) {
	screenname = address.split("/")[address.split("/").length - 1];
	d3.select("#main-container")
		.append("a")
	    .classed("twitter-timeline", true)
	    .classed("module-container", true)
	    .attr("id","twitter-timeline")
	    .attr("href", address);
	twttr.widgets.createTimeline(
	  {
	    sourceType: "profile",
	    screenName: screenname
	  },
	  document.getElementById("twitter-timeline"),
	  {
	  	height: "800"
	  }
	);
}








function initFacebookFeed() {
	pagelink = encodeURIComponent("https://www.facebook.com/JustinPJTrudeau");
	d3.select("#main-container")
		.append("iframe")
		.classed("module-container", true)
		.attr("id", "facebook-timeline")
		.attr("src", "https://www.facebook.com/plugins/page.php?href=" + pagelink + "&tabs=timeline&width=340&height=800&small_header=false&adapt_container_width=true&hide_cover=true&show_facepile=false&appId")
		.attr("width", "340")
		.attr("height", "800")
		.attr("style", "border:none;overflow:hidden")
		.attr("scrolling", "no")
		.attr("frameborder", "0")
		.attr("allowTransparency", "true");
}