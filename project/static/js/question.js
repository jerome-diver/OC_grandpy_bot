
$(document).ready(function() {
  $('form').on('submit', function(event) {
    $('#success-alert').text("Ok, j'analyse vôtre question et je cherche dans ma mémoire phénoménale quelles pourraient être les réponses les plus appropriées").show();
    $.ajax({
      data: { question: $('textarea#question').val() },
      type: 'POST',
      url: '/question' })
    .done(function(data) {
      if (data.error) {
        $('#error-alert').text(data.error).show();
        $('#success_alert').hide()
      } else {
        $('#answer').html(data.answer);
        $('#error-alert').hide()
        if ($('#answer').is(':empty')) {
          $('#warning-alert').text("Hélas, ma mémoire me fait défaut, je suis très vieux.").show();
        } else {
          $('#warning-alert').text("J'ai trouvé quelque chose mon grand...")
          .show();
        }
        $('#success-alert').fadeOut(2000);
        $('#warning-alert').fadeOut(4000);
      }
    });
    event.preventDefault();
  });
});