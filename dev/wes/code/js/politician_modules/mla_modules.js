var mppxmlpath = "/OntarioMPPSocial.xml"


function initTwitter(pid) {
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
		loadTwitterFeed(pid, twttr);
	});
}



function loadTwitterFeed(pid, twttr) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            let mlas = docXML.getElementsByTagName("MPP");
            for (let i = 0; i < mlas.length; i++) {
            	if (mlas[i].getAttribute("id") == pid) {
            		let screenname = mlas[i].getElementsByTagName("TwitterHandle")[0].childNodes[0].nodeValue;
            		twttr.widgets.createTimeline(
					  {
					    sourceType: "profile",
					    screenName: screenname
					  },
					  document.getElementById("bx-page-html-container"),
					  {
					  	height: "800"
					  }
					);
            	}
            }
    	}
  	};
  	xhttp.open("GET", mppxmlpath, true);
  	xhttp.send();
}