document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.getElementById('like-button');
    const likeCount = document.getElementById('like-count');
    let liked = likeButton.getAttribute('data-liked') === 'true';

    likeButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (!isAuthenticated) {
            alert('Пожалуйста, авторизуйтесь, чтобы ставить лайки.');
            return;
        }

        liked = !liked;
        likeButton.setAttribute('data-liked', liked);

        fetch('/like/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                content_type: likeButton.getAttribute('data-content-type'),
                object_id: likeButton.getAttribute('data-object-id')
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);
            likeCount.textContent = data.like_count;
        })
        .catch(error => console.error('Ошибка:', error));
    });
});