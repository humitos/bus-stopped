function setMarkers(map, locations) {
    
    var shape = {
	coord: [0, 0, 21, 25],
	type: 'rectangle'
    };

    for (var i = 0; i < locations.length; i++) {
	var point = locations[i];

	var infowindow = new google.maps.InfoWindow(
	    {
		content: point[2]
            });

	var myLatLng = new google.maps.LatLng(point[0], point[1]);
	var marker = new google.maps.Marker(
	    {
		position: myLatLng,
		map: map,
		shadow: point[3],
		icon: point[3],
		shape: shape,
		title: point[4],
		zIndex: 1
	    });

	// FIXME: those event's don't work propertly
	google.maps.event.addListener(marker, 'click', 
		function() {
		    infowindow.open(map, marker);
		});
	google.maps.event.addListener(map, 'dblclick', 
		function(event) {
		    placeMarker(map, event.latLng);
		});
    }
}

function placeMarker(map, location) {
    var clickedLocation = new google.maps.LatLng(location);
    var marker = new google.maps.Marker({
	position: location, 
	map: map
    });
}


function initialize() {
    var myOptions = {
	zoom: 13,
	center: new google.maps.LatLng(-31.74121, -60.5125),
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
                                  myOptions);

    {{ icons }}
    {{ maps }}
    setMarkers(map, locations);
}
