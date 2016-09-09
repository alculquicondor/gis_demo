var mymap = L.map('mapid').setView([-10, -75], 6);

L.tileLayer('/api/base_layer/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
}).addTo(mymap);

$.get('/api/areas', function (markers) {
  /*markers = markers.features;
  for ( var i=0; i < markers.length; ++i ) {
    var coords = markers[i].geometry.coordinates;
    L.marker( [coords[0], coords[1]] )
        .bindPopup( markers[i].properties.name )
        .addTo( mymap );
  }*/
  console.log(markers);
})

var capture = 0;
var capturedData = [];
var allPolygons = [];


function onMapClick(e) {
    if (capture) {
      capturedData.push(e.latlng);
      console.log('Data captured', e.latlng);
      capture--;
      if (!capture) {
        var p = L.polygon(capturedData)
        p.addTo( mymap );
        allPolygons.push(p)
        capturedData = [];
      }
      return;
    }
    console.log('Not capturing..')
}

function getPolygon(){
  capture = 4;
  console.log('Starting capture')  
}



mymap.on('click', onMapClick);

function send() {
  var p = allPolygons.map(function (p) {
    return p.toGeoJSON();
  });
  p.forEach(function(poly) {
  	$.post('/api/areas/create',poly,function(){
  		console.log(arguments);
  	})
  })
}

function clean(){
	console.log('Tengo que limpiar el mapa');
}