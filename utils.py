import settings

from pymaps import Map, PyMap, Icon

def buildmap(coord_list=[], center=(-31.73975, -60.5114), zoom=13):
    """
    Create javascript code to add to a template.
    This will contain the necessary items to build an entire
    Google Map.
    We could pass a list of dictionaries like this
    [{'title': 'Open CutHair',
      'icon': 'info',
      'latitude': x1,
      'longitude': x2,
      'address': '47 Street, CA',
      'description': 'Bv Sarmiento',
      }
    ]
    """

    icons = {
        'info': 'info.png' ,
        'building': 'building.png',
        }

    # Create a single map and set a quite large zoom level
    tmap = Map()
    tmap.zoom = zoom
    tmap.center = center
    tmap.points = []

    for point in coord_list:
        pointhtml = '<b>%s</b>' % point['title']
        pointhtml += "<br />" + "<br />".join([point['address'], point['description']])
        # pointhtml += "<br /><a href=\"/puntos_de_venta/report/%s/\">Reportar punto de venta mal ubicado</a>" % point[2]
                    # iconSize=(14,24), shadowSize=(23,21))
        tmap.setpoint((point['latitude'],
                       point['longitude'],
                       pointhtml,
                       'icon_' + point['icon'],
                       point['title']))

    # Create a google map with our items
    gmap = PyMap(maplist=[tmap])

    for k, v in icons.iteritems():
        icon = Icon(id='icon_' + k,
                    shadow=settings.MEDIA_URL + 'img/gmarkers/shadow.png',
                    shadow_size=(52, 29),
                    image=v,
                    image_size=(21, 31))
        gmap.addicon(icon)

    # Export javascript to build the map
    mapcode = gmap.pymapjs()
    return mapcode
