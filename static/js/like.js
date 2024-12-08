$(document).ready(function() {
    var $likeButton = $('#like-button');

    // Устанавливаем начальный стиль кнопки в зависимости от состояния
    // if ($likeButton.attr('data-liked') === 'true') {
    //     $likeButton.removeClass('like-active')
    // } else {
    //     $likeButton.addClass('like-active');
    // }

    // Обработчик клика на кнопке лайка
    $likeButton.click(function(event) {
        event.preventDefault();
        var $this = $(this);
        var liked = $this.attr('data-liked') === 'true';
        var contentType = $this.data('content-type');
        var objectId = $this.data('object-id');

        // Сразу меняем состояние на клиенте
        liked = !liked;
        $this.attr('data-liked', liked);

        // Обновляем класс кнопки
        if (liked) {
            $this.removeClass('like-active')
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
                $('#like-count').text(response.like_count);
            },
            error: function(xhr, status, error) {
                console.error("Ошибка при обработке лайка:" + status + error);
                // Восстанавливаем предыдущее состояние в случае ошибки
                $this.attr('data-liked', !liked);
                if (liked) {
                    $this.removeClass('btn-primary').addClass('btn-outline-primary');
                } else {
                    $this.removeClass('btn-outline-primary').addClass('btn-primary');
                }
            }
        });
    });
});
