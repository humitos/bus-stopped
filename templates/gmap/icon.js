// Origins, anchor positions and coordinates of the marker
// increase in the X direction to the right and in
// the Y direction down.
var {{ icon.id }} = new google.maps.MarkerImage('{{ MEDIA_URL }}img/gmarkers/{{ icon.image }}',
						// This marker is 20 pixels wide by 32 pixels tall.
						new google.maps.Size({{ icon.icon_size.0 }}, {{ icon.icon_size.1 }}),
						// The origin for this image is 0,0.
						new google.maps.Point(0,0),
						// The anchor for this image is the base of the flagpole at 0,32.
						new google.maps.Point({{ icon.icon_anchor.0 }}, {{ icon.icon_anchor.1 }}));

var {{ icon.id }}_shadow = new google.maps.MarkerImage(
    '{{ MEDIA_URL }}img/gmarkers/{{ icon.shadow }}',
    // The shadow image is larger in the horizontal dimension
    // while the position and offset are the same as for the main image.
    new google.maps.Size({{ icon.shadow_size.0 }}, {{ icon.shadow_size.1 }}),
    new google.maps.Point(0,0),
    new google.maps.Point({{ icon.icon_anchor.0 }}, {{ icon.icon_anchor.1 }}));

    // Shapes define the clickable region of the icon.
    // The type defines an HTML <area> element 'poly' which
    // traces out a polygon as a series of X,Y points. The final
    // coordinate closes the poly by connecting to the first
    // coordinate.
