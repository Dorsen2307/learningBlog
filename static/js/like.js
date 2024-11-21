/**
 * @typedef {Object} LikeResponse
 * @property {number} likes_count
 */

/**
 * @type {HTMLElement[]} */
document.querySelectorAll('.like').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const appLabel = this.getAttribute('data-app-label');
        const modelName = this.getAttribute('data-model-name');
        const objectId = this.getAttribute('data-object-id');

        fetch(`/like/${modelName}/${objectId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then((/** @type {LikeResponse} */ data) => {
            // Обновляем количество лайков на странице
            this.nextElementSibling.textContent = data.likes_count;
        })
        .catch(error => console.error('Ошибка:', error));
    });
});