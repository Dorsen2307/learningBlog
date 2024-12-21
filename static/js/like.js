$(document).ready(function() {
    var $likeButton = $('.like-btn');

    // Инициализация кнопок лайк
    $likeButton.each(function() {
        var $this = $(this);
        if ($this.attr('data-liked') === 'true') {
            $this.removeClass('like-active');
        } else {
            $this.addClass('like-active');
        }
    });

    // Обработчик клика на кнопке лайка
    $likeButton.click(function(event) {
        event.preventDefault();
        var $this = $(this);
        var liked = $this.attr('data-liked') === 'true';
        var contentType = $this.data('content-type');
        var objectId = $this.data('object-id');
        console.log(contentType)
        // Сразу меняем состояние на клиенте
        liked = !liked;
        $this.attr('data-liked', liked);

        // Обновляем класс кнопки
        if (liked) {
            $this.removeClass('like-active');
        } else {
            $this.addClass('like-active');
        }

        $.ajax({
            url: "/like/",
            method: "POST",
            data: {
                'content_type': contentType,
                'object_id': objectId,
                'liked': liked,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                // Обновляем счетчик лайков
                $('#like-count-' + objectId).text(response.like_count);
            },
            error: function(xhr, status, error) {
                console.error("Ошибка при обработке лайка:" + status + error);
                console.error("Ответ сервера: " + xhr.responseText);
                // Восстанавливаем предыдущее состояние в случае ошибки
                $this.attr('data-liked', !liked);
                if (liked) {
                    $this.removeClass('like-active');
                } else {
                    $this.addClass('like-active');
                }
            }
        });
    });
});
