$(document).ready(function () {
  $('#send').click(function (e) {
      e.stopPropagation();
      var user_input = $('#user_input').val();
      if (user_input.trim() !== '') {
              $.ajax({
                  url: '{% url "chatbot"%}',
                  type: 'POST',
                  data: {
                      'user_input': user_input,
                      'csrfmiddlewaretoken': '{{ csrf_token }}',
                  },
                  success: function (data) {
                      $('#messages').append('<div><strong>You:</strong> ' + user_input + '</div>');
                      $('#messages').append('<div><strong>AI:</strong> ' + data.response + '</div>');
                      $('#user_input').val('');
                      $('#messages').scrollTop($('#messages')[0].scrollHeight);
                  },
                  error: function (xhr, status, error) {
                      console.error(error);
                  },
              });
          }
      });
  });
