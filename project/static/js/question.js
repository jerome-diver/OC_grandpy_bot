
$(document).ready(function() {
  function initMap(location) {
    var mapCanvas = document.getElementById('map');
    var mapOptions = {
      center: location,
      zoom: 16,
      panControl: false,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
  }

  function getLocationFromAddress(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
      if (status === 'OK') {
        return results[0].geometry.location;
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
        return null;
      }
    });
  }

  function getLocationFromCoordinates(latitude, longitude) {
    return new google.maps.LatLng(latitude, longitude);
  }

  google.maps.event.addDomListener(window, 'load', initMap);

  $('form').on('submit', function(event) {
    $("#submit").hide();
    $("#loading").show();
    $.ajax({
      data: { 'question': $('textarea#question').val() },
      type: 'POST',
      url: '/question' })
    .done(function(data) {
      $("#submit").show();
      $("#loading").hide();
      $('#messages').html(data.messages);
      $("#messages").show();
      $("#messages").fadeIn(500);
      $('#messages').fadeOut(4000);
      if (data.error) {
        console.log("Error")
      } else {
        $('#result').html(data.result);
        if (data.latitude != '') {
          initMap(getLocationFromCoordinates(data.latitude,
                                             data.longitude));
        }
        else {
          initMap(getLocationFromAddress(data.address));
        }
      }
    });
    event.preventDefault();
  });
});
