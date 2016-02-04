function initMap() {
   
 var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 48.578333, lng: 19.123333},
    zoom: 8
  });
  
var marker;

function placeMarker(location) {
  if ( marker ) {
    marker.setPosition(location);
  } else {
    marker = new google.maps.Marker({
      position: location,
      map: map
    });
  }
  document.getElementById("lat").value = location.lat();
  document.getElementById("lng").value =location.lng();
}
google.maps.event.addListener(map, 'click', function(event) {
  placeMarker(event.latLng);
  
  });

  
}
var vytvorenieMapa = function(){
   
    
    initMap();
   
}

var nastavenie = function(){
    vytvorenieMapa();
    
    
}

$(document).ready(nastavenie);