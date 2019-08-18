
$(document).ready(function() {
  function initMap(latitude, longitude) {
    if (!latitude) {
      latitude = 50.45875;
      longitude = 7.5446;
    }
    var location = new google.maps.LatLng(latitude, longitude);
    var mapCanvas = document.getElementById('map');
    var mapOptions = {
      center: location,
      zoom: 16,
      panControl: false,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
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
        $('#answer').html(data.answer);
        initMap(data.latitude, data.longitude)
      }
    });
    event.preventDefault();
  });
});
