const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
const botAjaxError = "bot can't said anything... AJAX ERROR";
const userAjaxError = "user can't said anything... AJAX ERROR";

const loading = () => {
  $("#submit").hide();
  $("#loading").show();
}

const endLoading = () => {
  $("#submit").show();
  $("#loading").hide();
}

const flash = (content) => {
  $('#messages').html(data.messages);
  $("#messages").show();
  $("#messages").fadeIn(500);
  $('#messages').fadeOut(4000);
}

const ask = (content, type, index) => {
  $.ajax({
    data: { 'question': content, 'type': type, 'index': index },
    type: 'POST',
    url: '/question' })
  .done( (data) => {
    $("input#question").val('');
    endLoading();
    flash(content);
    if (data.error) {
      console.log("Error")
    } else {
      botSaid(data.answer);
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
      } else { console.log("Nothing found") }
    }
  });
}

const botSaid = (content) => {
  $.ajax({
    url: "/bot_said",
    data: { 'answer': content,
            'time': moment().format('LTS'),
            'location': tz},
    type: "POST",
    success: (response) => { $("#chat").append(response.answer) },
    error: (xhr) => { console.log( botAjaxError ) }
  });
}

const userSaid = (content) => {
  $.ajax({
    url: "/user_said",
    data: { 'question': content,
            'time': moment().format('LTS'),
            'location': tz },
    type: "POST",
    success: (response) => { $("#chat").append(response.question) },
    error: (xhr) => { console.log( userAjaxError) }
  });
}

$(document).ready( () => {
  console.log(tz);
  console.log(moment().format('LTS'))
  const initMap = (location) => {
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

  const getLocationFromAddress = (address) => {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, (results, status) => {
      if (status === 'OK') { return results[0].geometry.location }
      else {
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

  const getLocationFromCoordinates = (latitude, longitude) => {
    return new google.maps.LatLng(latitude, longitude);
  }

  const mark = (map, location, title, content) => {
    var infoWindow = new google.maps.InfoWindow({ content: content });
    var marker = new google.maps.Marker({
                map: map,
                position: location,
                animation: google.maps.Animation.BOUNCE,
                label: title
              });
    marker.addListener('click', () => { infoWindow.open(map, marker) });
  }

  google.maps.event.addDomListener(window, 'load', initMap);

  $("#dialog-question").on('submit', (event) => {
    loading();
    userSaid($('input#question').val())
    ask($('input#question').val(), "question", 0 );
    event.preventDefault();
  });
});

$(document).on('click', '.dialog-answer', (event) => {
  const id = event.target.id
  const content = $(event.target).text();
  console.log('id: ', id, ' content: ', content.trim());
  loading();
  userSaid(content.trim());
  ask(content, "answer", id);
});
