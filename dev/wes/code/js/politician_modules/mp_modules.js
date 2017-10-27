
//*******************************************************************************************
//
//		VOTING RECORD MODULE
//
//*******************************************************************************************

$(document).ready(function() {
	loadMPDatabase("../../../data/government/mp_list.xml");
	var maincontainer = d3.select("#main-container");
	var votingmodule = maincontainer.append("div").classed("module-container", true).attr("id", "mp-voting-record");
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