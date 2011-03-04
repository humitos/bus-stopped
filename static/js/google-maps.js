$(document).ready(function(){
                      // center: new google.maps.LatLng(-31.74121, -60.5125),
                      initialLocation = new google.maps.LatLng(-31.74141804574782, -60.51123228454588);
                      myOptions = {
                          zoom: 13,
                          center: initialLocation,
                          mapTypeId: google.maps.MapTypeId.ROADMAP
                      };

                      map = new google.maps.Map(document.getElementById("map_canvas"),
                                                myOptions);
                      bounds = new google.maps.LatLngBounds();
		      
		      // arrays to save the items
		      markers = [];
		      layers = [];
		      last_info_window = new google.maps.InfoWindow();
                  });

function loadBusStop(line, direction) {
    var url = '/ajax/busstopped/';
    url += line + '/' + direction;

    $.each(markers, function(i, marker){
    	       marker.setMap(null);
    	   });

    $.getJSON(url, function(data){
                  // Shape over the icon we can click
                  // var shape = {
                  //     coord: [0, 0, 21, 31],
                  //     type: 'rectangle'
                  // };
                  var shape = {
                      coord: [16, 16, 16],
                      type: 'circle'
                  };

                  $.each(data, function(i, point){
                             var myLatLng = new google.maps.LatLng(point['latitude'], point['longitude']);
                             var marker = new google.maps.Marker(
                                 {
                                     clickable: true,
                                     position: myLatLng,
                                     map: map,
                                     shadow: point.shadow,
                                     icon: point.icon,
                                     shape: shape,
                                     title: point.name,
                                     zIndex: 1,
                                     key: point.key,
				     address: point.address
                                 });
			     markers.push(marker);

                             bounds.extend(myLatLng);
                             google.maps.event.addListener(marker, 'click',
                                                           function(event) {
							       last_info_window.close();
                                                               $.getJSON('/ajax/point?busstop_key=' + marker.key, function(data){
                                                                             var content = '<b>' + marker.title + '</b> ';
									     content += marker.address;
                                                                             $.each(data, function(i, bus_time){
                                                                                        content += '<br /><b>' + bus_time.time_left  + ' min:</b> ' + bus_time.direction  + ' <span>' + bus_time.time + '</span>';
                                                                                    });
                                                                             var infowindow = new google.maps.InfoWindow(
                                                                                 {
                                                                                     content: content
                                                                                 });
                                                                             infowindow.open(map, marker);
									     last_info_window = infowindow;
                                                                         });

                                                           });
                         });
              });
}

function initialize() {

    loadBusStop('6', 'Ida');
    // map.fitBounds(bounds);

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

function getMyLocation(){
    var geocoder = new google.maps.Geocoder();
    var address = $("input[name='user-location']").val();
    var original_address = address;
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
                                            title: original_address,
                                            zIndex: 1
                                        });
                                    map.setCenter(result['geometry'].location);
                                });
                     });
}

var near_busstop = 0;
function getNearBusStop(){
    var lat = $("input[name='latitude']").val();
    var lng = $("input[name='longitude']").val();
    var origin = new google.maps.LatLng(lat, lng);

    var ds = new google.maps.DirectionsService();
    var minor_distance = 50000;

    $.getJSON('/ajax/busstopped', 
              function(data){
                  $.each(data,
                         function(i, item){
                             var destination = new google.maps.LatLng(item['latitude'], item['longitude']);
                             ds.route({
                                          destination: destination,
                                          origin: origin,
                                          travelMode: google.maps.DirectionsTravelMode.WALKING,
                                          provideRouteAlternatives: false
                                      },
                                      function(result, status){
                                          alert('insite ' + this.near_busstop);
                                          var distance = result.routes[0].legs[0].distance.value;
                                          if(distance < minor_distance){
                                              minor_distance = distance;
                                              near_busstop = item;
                                          }
                                      });
                         });

                  var location = new google.maps.LatLng(near_busstop['latitude'], near_busstop['longitude']);
                  var marker = new google.maps.Marker(
                      {
                          clickable: true,
                          position: location,
                          map: map,
                          shadow: '/static/img/gmarkers/shadow.png',
                          icon: '/static/img/gmarkers/building.png',
                          title: 'Near Bus Stop',
                          zIndex: 2
                      });
              });
}

function KmlLayer(){
    var line = $('select[name=path-line] option:selected').val();
    var direction = $('select[name=path-direction] option:selected').val();
    // This .kml MUST be in public domain
    var url = window.location.href;
    // FIXME: Just for DEBUG
    if(url.indexOf('localhost') >= 0){
	url = 'http://humitos.homelinux.net:8007/';
    }
    url += 'static/kml/' + direction + '_linea_' + line + '.kmz';

    // $.each(layers, function(i, layer){
    // 	       layer.setMap(null);
    // 	   });

    var kml_layer = new google.maps.KmlLayer(url,
                                             {preserveViewport: true, suppressInfoWindows:true});
    kml_layer.setMap(map);
    layers.push(kml_layer);
}
