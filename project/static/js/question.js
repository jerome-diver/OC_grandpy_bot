const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;

class Dialog {
  constructor(user, bot) {
    this.user = user;
    this.bot = bot;
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
        if (data.found == 1) {
          this.bot.said(data.answer, data.map_id,
                        data.title, data.resume);
          $('#result').html(data.result);
          $('.choices').prop("disabled",true);
        }
        else if (data.found == 2) {
          $('#result').html(data.result);
          this.bot.said(data.answer, null, null, null)
        }
        else {
          this.bot.said(data.result, null, null, null)
        }
      }
    });
  }
}

class Bot {
  constructor() {
    this.ajaxError = "bot can't said anything... AJAX ERROR";
    this.ajaxCoordinatesError = "There is no AJAX coordinate for a map.";
  }

  said(content, map_id, title, resume) {
    $.ajax({
      url: "/bot_said",
      data: { 'answer': content,
              'time': moment().format('LTS'),
              'location': tz,
              'mapid': map_id},
      type: "POST",
      success: (response) => {
        $("#chat").append(response.answer)
        if (map_id != null) {
          $.ajax({
            url: "/map_coordinates",
            type: "GET",
            success: (data) => {
              var location = null;
              if (data.latitude != '') {
                console.log("search from latitude/longitude returned");
                location = GoogleMap.locationFromCoordinates(data.latitude,
                                                             data.longitude);
              }
              else if (data.address != '') {
                console.log("Search from address returned");
                location = GoogleMap.locationFromAddress(data.address);
              }
              console.log("Location found is ", location);
              const map_id = "map_" + data.map_id;
              var map = new GoogleMap(location, map_id);
              map.mark(location, title, resume);
            },
            error: (xhr) => { console.log( this.ajaxCoordinatesError ) }
          });
        }
      },
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
  constructor(location, id) {
    console.log("New GoogleMap with id =", id);
    this.map = this.initMap(location, id);
    google.maps.event.addDomListener(window, 'load', this.map);
  }

  initMap(location, id) {
    var mapCanvas = document.getElementById(id);
    var mapOptions = {
      center: location,
      zoom: 16,
      panControl: false,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    return new google.maps.Map(mapCanvas, mapOptions);
  }

  static locationFromAddress(address) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, (results, status) => {
      if (status === 'OK') { return results[0].geometry.location }
      else {
        alert('Geocode was not successful for the following reason: ${status}');
        return null;
      }
    });
  }

  static locationFromCoordinates(latitude, longitude) {
    return new google.maps.LatLng(latitude, longitude);
  }


  mark(location, title, content) {
    this.infoWindow = new google.maps.InfoWindow({ content: content });
    this.marker = new google.maps.Marker({
                map: this.map,
                position: location,
                animation: google.maps.Animation.BOUNCE,
                label: title
              });
    this.marker.addListener('click', () => { infoWindow.open(this.map, marker)
    });
  }
}

$(document).ready( () => {
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

