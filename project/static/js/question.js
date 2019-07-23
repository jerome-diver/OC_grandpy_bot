
$(document).ready(function() {
  $f('form').on('submit', function(event) {
    $.ajax({
      question: $('#question').val();
    })
    .done(function(data){
      if (data.error) {
        $('#error-alert').text(data.error).show();
        $('#success_alert').hide()
      } else {
        $('#error-alert').hide()
        $('#success_alert').text(data.question).show();
        pass
      }
    });
    event.preventDefault():
  });
});