$(document).ready(function(){
		      myOptions = {
			  zoom: 13,
			  center: new google.maps.LatLng(-31.74121, -60.5125),
			  mapTypeId: google.maps.MapTypeId.ROADMAP
		      };
		      
		      map = new google.maps.Map(document.getElementById("map_canvas"),
						myOptions);
		      bounds = new google.maps.LatLngBounds();
		  });

function initialize() {

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

    // map.fitBounds(bounds);

    // Add a point
    google.maps.event.addListener(map, 'click', 
				  function(event) {
				      $('input[name="latitude"]').attr('value', event.latLng.lat());
				      $('input[name="longitude"]').attr('value', event.latLng.lng());
				  });
}

function getDirection(){
    var origin_lat = $("input[name='latitude']").val();
    var origin_lng = $("input[name='longitude']").val();

    var originLatLng = new google.maps.LatLng(origin_lat, origin_lng);
    var destinationLatLng = new google.maps.LatLng(-31.72699803750814, -60.51389743088009);
    var direction_service = new google.maps.DirectionsService();
    direction_service.route({
				destination: destinationLatLng,
				origin: originLatLng,
				provideRouteAlternatives: true,
				travelMode: google.maps.DirectionsTravelMode.WALKING
			    },
			   function(direction_result, direction_status){
			       var directions_renderer = new google.maps.DirectionsRenderer({
												directions: direction_result,
												map: map,
												preserveViewport: true
											  });
			       
			   });
}

function getBusStop(){
    var geocoder = new google.maps.Geocoder();
    var address = $("input[name='user-location']").val();
    address += ' Parana, Entre Rios';
    
    geocoder.geocode({
			 address: address,
			 bounds: bounds
		     },
		     function(geocoder_result, geocoder_status){
			 $.each(geocoder_result, function(i, result){
				    var marker = new google.maps.Marker(
					{
					    clickable: true,
					    position: result['geometry'].location,
					    map: map,
					    shadow: '/static/img/gmarkers/shadow.png',
					    icon: '/static/img/gmarkers/building.png',
					    title: 'Busqueda',
					    zIndex: 1
					});
				});
		     });
}