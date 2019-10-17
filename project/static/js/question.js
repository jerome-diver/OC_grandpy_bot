const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;

class Dialog {
  constructor(user, bot) {
    this.user = user;
    this.bot = bot;
    this.map = new GoogleMap();
  }
  static loading() {
    $("#submit").hide();
    $("#loading").show();
  }

  static endLoading() {
    $("#submit").show();
    $("#loading").hide();
  }

  static flash(content) {
    $('#messages').html(content);
    $("#messages").show();
    $("#messages").fadeIn(500);
    $('#messages').fadeOut(4000);
  }

  submit(content, type, index) {
    Dialog.loading();
    $.ajax({
      data: { 'question': content, 'type': type, 'index': index },
      type: 'POST',
      url: '/submit' })
    .done( (data) => {
      $("input#question").val('');
      Dialog.endLoading();
      Dialog.flash(content);
      if (data.error) {
        console.log("Error")
      } else {
        this.bot.said(data.answer);
        if (data.found == 1) {
          $('#result').html(data.result);
          var location = null;
          if (data.latitude != '') {
            console.log("search from latitude/longitude returned");
            location = this.map.getLocationFromCoordinates(data.latitude,
                                                           data.longitude);
          }
          else if (data.address != '') {
            console.log("Search from address returned");
            location = this.map.getLocationFromAddress(data.address);
          }
          console.log("Location found is ", location);
          var map = this.map.initMap(location);
          this.map.mark(map, location, data.title, data.resume)
        }
        else if (data.found == 2) {
          $('#result').html(data.result);
        }
        else { console.log("Nothing found") }
      }
    });
  }
}

class Bot {
  constructor() {
    this.ajaxError = "bot can't said anything... AJAX ERROR";
  }

  said(content) {
    $.ajax({
      url: "/bot_said",
      data: { 'answer': content,
              'time': moment().format('LTS'),
              'location': tz},
      type: "POST",
      success: (response) => { $("#chat").append(response.answer) },
      error: (xhr) => { console.log( this.ajaxError ) }
    });
  }
}

class User {
  constructor() {
    this.ajaxError = "user can't said anything... AJAX ERROR";
  }

  said(content) {
    $.ajax({
      url: "/user_said",
      data: { 'question': content,
              'time': moment().format('LTS'),
              'location': tz },
      type: "POST",
      success: (response) => { $("#chat").append(response.question) },
      error: (xhr) => { console.log( this.ajaxError) }
    });
  }
}

class GoogleMap {
  constructor() {
    this.initMap = (location) => {
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
    google.maps.event.addDomListener(window, 'load', this.initMap);
  }

  getLocationFromAddress(address) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, (results, status) => {
      if (status === 'OK') { return results[0].geometry.location }
      else {
        alert('Geocode was not successful for the following reason: ' + status);
        return null;
      }
    });
  }

  getLocationFromCoordinates(latitude, longitude) {
    return new google.maps.LatLng(latitude, longitude);
  }


  mark(map, location, title, content) {
    var infoWindow = new google.maps.InfoWindow({ content: content });
    var marker = new google.maps.Marker({
                map: map,
                position: location,
                animation: google.maps.Animation.BOUNCE,
                label: title
              });
    marker.addListener('click', () => { infoWindow.open(map, marker) });
  }
}

$(document).ready( () => {
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
  const user = new User();
  const bot = new Bot();
  const dialog = new Dialog(user, bot);

  $("#dialog-question").on('submit', (event) => {
    user.said($('input#question').val())
    dialog.submit($('input#question').val(), "question", 0 );
    event.preventDefault();
  });

  $(document).on('click', '.dialog-answer', (event) => {
    const id = event.target.id
    const content = $(event.target).text();
    console.log('id: ', id, ' content: ', content.trim());
    user.said(content.trim());
    dialog.submit(content, "answer", id);
  });

});

