$('#comment-form').submit(function(event) {
    event.preventDefault();

    var username = $('#username').val();
    var comment = $('#comment').val();
    $.ajax({
        url: 'http://127.0.0.1:5000/', 
        method: 'POST',
        data: {
            username: username,
            comment: comment
        },
        success: function(response) {
            console.log('Ответ от сервера (POST):', response);
            loadComments(); 
            $('#comment-form')[0].reset();
        },
        error: function(xhr, status, error) {
            console.log('Ошибка при отправке комментария:', status, error); 
        }
    });
});

function loadComments() {
    $.get('http://127.0.0.1:5000/', function(data) {
        console.log('Полученные данные от сервера (GET):', data);  

        $('#comments-container').empty(); 

        if (data.comments && data.comments.length > 0) {
            data.comments.forEach(function(comment) {
                var commentHTML = `
                    <div class="comment">
                        <strong>${comment.username}:</strong> <p>${comment.content}</p>
                    </div>
                `;
                $('#comments-container').append(commentHTML);
            });
        } else {
            $('#comments-container').append('<p>Комментариев нет.</p>');
        }
    }).fail(function(xhr, status, error) {
        console.log('Ошибка при загрузке комментариев:', status, error);  
        $('#comments-container').append('<p>Ошибка загрузки комментариев. Попробуйте позже.</p>');
    });
}

$(document).ready(function() {
    loadComments();  
});             