
$(document).ready(function() {
  $('form').on('submit', function(event) {
    $('#success-alert').text("Ok, j'analyse vôtre question et je cherche dans ma mémoire phénoménale quelles pourraient être les réponses les plus appropriées").show();
    $.ajax({
      data: { 'question': $('textarea#question').val() },
      type: 'POST',
      url: '/question' })
    .done(function(data) {
      $('#messages').html(data.messages);
      $("#messages").show();
      $("#messages").fadeIn(500);
      $('#messages').fadeOut(2000);
      if (data.error) {
        console.log("Error")
      } else {
        $('#answer').html(data.answer);
      }
    });
    event.preventDefault();
  });
});