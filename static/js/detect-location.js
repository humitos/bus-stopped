var initialLocation;
var parana = new google.maps.LatLng(-31.74141804574782, -60.51123228454588);
var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
var browserSupportFlag =  new Boolean();

// Try W3C Geolocation (Preferred)
if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
						 initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
						 map.setCenter(initialLocation);
					     }, function() {
						 handleNoGeolocation(browserSupportFlag);
					     });
    // Try Google Gears Geolocation
} else if (google.gears) {
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
			       initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
			       map.setCenter(initialLocation);
			   }, function() {
			       handleNoGeoLocation(browserSupportFlag);
			   });
    // Browser doesn't support Geolocation
} else {
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
}

function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
	alert("Geolocation service failed.");
	initialLocation = newyork;
    } else {
	// alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
	initialLocation = parana;
    }
}
