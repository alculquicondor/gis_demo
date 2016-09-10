var mymap = L.map('mapid').setView([-10, -75], 6);

L.tileLayer('/api/base_layer/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
}).addTo(mymap);

$.get('/api/areas', function (markers) {
  var mrks = markers.features.forEach(function (f) {
  	var points = f.geometry.coordinates[0].map(function (p) {
  		return {
  			lat: p[1],
  			lng: p[0]
  		}
  	})
  	var p = L.polygon(points)
  	p.addTo( mymap );
  })
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
        p = p.toGeoJSON();
        p.properties.name = prompt('Write a label for this polygon');
        console.log(p);
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
  	return p;
  });
  p.forEach(function(poly) {
  	$.ajax('/api/areas/create', {
	    data : JSON.stringify(poly),
	    contentType : 'application/json',
	    type : 'POST'
	}).done(function () {
		console.log(arguments);
	})
  })
}

function getResults(){
  $.get('/api/areas', function (markers) {
  var mrks = markers.features.forEach(function (f) {
  	var points = f.geometry.coordinates[0].map(function (p) {
  		return {
  			lat: p[1],
  			lng: p[0]
  		}
  	})
  	var p = L.polygon(points,{color: 'red'});
  	p.addTo( mymap );
  })
})

}