function ask(content, type, index) {
  $.ajax({
    data: { 'question': content, 'type': type, 'index': index },
    type: 'POST',
    url: '/question' })
  .done(function(data) {
    var old_question = content;
    $("input#question").val('');
    $("#submit").show();
    $("#loading").hide();
    $('#messages').html(data.messages);
    $("#messages").show();
    $("#messages").fadeIn(500);
    $('#messages').fadeOut(4000);
    if (data.error) {
      console.log("Error")
    } else {
      $.ajax({
        url: "/bot_said",
        data: { 'answer': data.answer },
        type: "POST",
        success: function(response) {
          $("#chat").append(response.answer);
        },
        error: function(xhr) {
          //Do Something to handle error
        }
      });
      if (data.found == 1) {
        $('#result').html(data.result);
        var location = null;
        if (data.latitude != '') {
          location = getLocationFromCoordinates(data.latitude,
                                                data.longitude);
        }
        else {
          location = getLocationFromAddress(data.address);
        }
        var map = initMap(location);
        mark(map, location, data.title, data.resume)
      }
      if (data.found == 2) {
        $('#result').html(data.result);
      } else {
        console.log("Nothing found");
      }
    }
  });

}

$(document).ready(function() {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  console.log(tz);
  console.log(moment().format('LTS'))
  function initMap(location) {

    var mapCanvas = document.getElementById('map');
    var mapOptions = {
      center: location,
      zoom: 16,
      panControl: false,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
    return map;
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

  //function getBrowserLocation() {
  //  if (navigator.geolocation) {
  //    navigator.geolocation.getCurrentPosition(
  //      function(position) {
  //        var pos = {
  //          lat: position.coords.latitude,
  //          lng: position.coords.longitude
  //        };

   //     }, function() {  });
   //  } else {
   //    // Browser doesn't support Geolocation
   //    //handleLocationError(false, infoWindow, map.getCenter());
   //  }
  //}

  //function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  //  infoWindow.setPosition(pos);
  //  infoWindow.setContent(browserHasGeolocation ?
  //                        'Error: The Geolocation service failed.' :
  //                        'Error: Your browser doesn\'t support geolocation
  //.');
  //  infoWindow.open(map);
  //}

  function getLocationFromCoordinates(latitude, longitude) {
    return new google.maps.LatLng(latitude, longitude);
  }

  function mark(map, location, title, content) {
  var infoWindow = new google.maps.InfoWindow({
          content: content });
  var marker = new google.maps.Marker({
              map: map,
              position: location,
              animation: google.maps.Animation.BOUNCE,
              label: title
            });
  marker.addListener('click', function() {
          infoWindow.open(map, marker); });
  }

  google.maps.event.addDomListener(window, 'load', initMap);

  $("#dialog-question").on('submit', function(event) {
    console.log("OK");
    $("#submit").hide();
    $("#loading").show();
    $.ajax({
      url: "/user_said",
      data: { 'question': $('input#question').val()},
      type: "POST",
      success: function(response) {
        $("#chat").append(response.question);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
    ask($('input#question').val(), "question", 0 );
    event.preventDefault();
  });
});

$(document).on('click', '.dialog-answer', function (event) {
    const id = event.target.id
    const content = $(event.target).text();
    console.log('id: ', id, ' content: ', content);
    ask(content, "answer", id);
});

