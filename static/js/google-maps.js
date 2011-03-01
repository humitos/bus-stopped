function initialize() {
    var myOptions = {
        zoom: 13,
        center: new google.maps.LatLng(-31.74121, -60.5125),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map_canvas"),
                                  myOptions);
    var bounds = new google.maps.LatLngBounds();

    $.getJSON('/ajax/busstopped', function(data){
		  // Shape over the icon we can click
		  // var shape = {
		  //     coord: [0, 0, 21, 31],
		  //     type: 'rectangle'
		  // };
		  var shape = {
		      coord: [10, 15, 10],
		      type: 'circle'
		  };
		  
		  $.each(data, function(i, point){
			     var myLatLng = new google.maps.LatLng(point['latitude'], point['longitude']);
			     var marker = new google.maps.Marker(
				 {
				     clickable: true,
				     position: myLatLng,
				     map: map,
				     shadow: point['shadow'],
				     icon: point['icon'],
				     shape: shape,
				     title: point['title'],
				     zIndex: 1
				 });
			     
			     // FIXME: those event's don't work propertly
			     var infowindow = new google.maps.InfoWindow(
				 {
				     content: point['description']
				 });
			     bounds.extend(myLatLng);
			     google.maps.event.addListener(marker, 'click', 
							   function(event) {
							       infowindow.open(map, marker);
							   });
			 });
	      });

    map.fitBounds(bounds);

    // Add a point
    google.maps.event.addListener(map, 'click', 
				  function(event) {
				      $('input[name="latitude"]').attr('value', event.latLng.lat());
				      $('input[name="longitude"]').attr('value', event.latLng.lng());
				  });
}

