

const colormap = {"blue-a" : "#3e96d6",
				  "green-a" : "#339b38",
				  "gray-a" : "#ccc",
				  "blue-b" : "#2e86c6",
				  "green-b" : "#238b28",
				  "gray-b" : "#aaa"};



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







class Visual {

	constructor(selectorId) {
		this._container = document.getElementById(selectorId);
		this._width = this._container.clientWidth;
		this._height = this._container.clientHeight;
		this._aspect = this._height / this._width;
	}

	get width() {
		return this._width;
	}

	get height() {
		return this._height;
	}

	get aspect() {
		return this._aspect;
	}

	get container() {
		return this._container;
	}

	set container(selectorId) {
		this._container = document.getElementById(selectorId);
		this._width = this.container.clientWidth;
		this._height = this.container.clientHeight;
		this._aspect = this._height / this._width;
	}

	set aspect(value) {
		this._aspect = value
		this._height = value * this._width;
	}

	set height(value) {
		this._height = value;
		this._aspect = this._height / this._width;
	}

	set width(value) {
		this._width = value;
		this._aspect = this._height / this._width;
	}

}



class TimeSeries extends Visual {

	constructor(selectorId, data, options={dateFormat: "%Y-%m-%d"}) {
		super(selectorId);
		this.data = data;
		this.options = options;
		this.svg = d3.select("selectorId").append("svg").attr("width", this.width).attr("height", this.height);
		this.margin = {top: 20, right: 80, bottom: 30, left: 50};
		this.chartwidth = svg.attr("width") - margin.left - margin.right;
		this.chartheight = svg.attr("height") - margin.top - margin.bottom;
		this.g = this.svg.append("g").attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

		this.parseTime = d3.timeParse(this.options.dateFormat);
		this.x = d3.scaleTime()
					.domain()
					.range([0, this.chartwidth]);
    	this.y = d3.scaleLinear()
    				.domain()
    				.range([this.chartheight, 0]);
    	this.z = d3.scaleOrdinal(d3.schemeCategory10)
    				.domain();
		this.line = d3.line()
		    			.curve(d3.curveBasis)
		    			.x(function(d) { return x(d.date); })
		    			.y(function(d) { return y(d.value); });


	}

	clearChart() {

	}

	resetChart(data) {

	}



}







//*******************************************************************************************
//
//		VOTING RECORD MODULE
//
//*******************************************************************************************




class PieChart extends Visual {

	constructor(data, selectorId) {
		super(selectorId);
		this.data = data;
		this.radius = Math.min(this.width, this.height) / 2;
	    this.svg = d3.select(this.container).append('svg')
	        					  .attr("id", "pieChartSVG")
	                              .attr('width', this.width)
	                              .attr('height', this.height);

	    this.pie = this.svg.append('g')
	                .attr(
	                  'transform',
	                  'translate(' + this.width / 2 + ',' + this.height / 2 + ')'
	                );

	    this.pieData = d3.pie()
	                    .value(function(d) {return d.value;}).padAngle(.02);

	    this.arc = d3.arc()
	                    .outerRadius(this.radius - 10)
	                    .innerRadius(0.6 * this.radius);
	}

	initChart() {
		var that = this;

	    this.pieChartPieces = that.pie.datum(that.data)
	                            .selectAll('path')
	                            .data(that.pieData)
	                            .enter()
	                            .append('path')
	                            .attr('class', function(d) {
	                              return 'pie-chart-segment pie-chart_' + d.data.title.toLowerCase();
	                            })
	                            .style("fill", function(d) {return colormap[d.data.color]})
	                            .attr('d', this.arc)
	                            .each(function() {
	                              this._current = {startAngle: 0, endAngle: 0};
	                            })
	                            .transition()
	                            .duration(600)
	                            .attrTween('d', function(d) {
	                              var interpolate = d3.interpolate(this._current, d);
	                              this._current = interpolate(0);

	                              return function(t) {
	                                return that.arc(interpolate(t));
	                              };
	                            })
	}

	eraseChart() {
		this.svg.remove();
	}

	resetChart() {
		this.eraseChart();
		this.initChart()
	}
}







function loadVotingRecord() {
	var piedata = [
      {
        color       : 'green-a',
        description : 'Member voted in favour of motion or bill.',
        title       : 'Yea',
        value       : 0.62
      },
      {
        color       : 'blue-a',
        description : 'Member voted in opposition to motion or bill.',
        title       : 'Nay',
        value       : 0.28
      },
      {
        color       : 'gray-a',
        description : 'Member was absent, abstained, or was paired for vote.',
        title       : 'None',
        value       : 0.1
      }
    ]
    var votingmodule = d3.select("#main-container").append("div").classed("module-container", true).attr("id", "voting-record");
	votingmodule.append("h2").text("Voting Record Module");
	var pie = new PieChart(piedata, "voting-record");
	pie.initChart();

	var ts = new TimeSeries("voting-record", {});
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
		.attr("src", "https://www.facebook.com/plugins/page.php?href=" + pagelink + "&tabs=timeline&small_header=false&adapt_container_width=true&hide_cover=true&show_facepile=false&appId")
		.attr("style", "border:none;overflow:hidden")
		.attr("scrolling", "no")
		.attr("width", "inherit")
		.attr("frameborder", 0)
		.attr("allowTransparency", "true");
}