// Вычисляем количество лет
function getAge(dateString) {
	var birthday = new Date(dateString); // дата рождения как объект
	var today = new Date(); // текущая дата как объект
	var month = today.getMonth() - birthday.getMonth(); //вычисляем число месяцев
	var age = today.getFullYear() - birthday.getFullYear(); // вычисляем число лет
	// выясняем меньше ли текущие день и месяц, чем день и месяц рождения, если да, то уменьшаем год на 1
	if (month < 0 || (month === 0 && today.getDate() < birthday.getDate())) {
		age--;
	}
	return age;
}

// Выбирем нужную фигуру по годам
function trueAge(age) {
	const imgElements = document.getElementsByClassName("main-age"); //находим тег img
	const opac = 0; //прозрачность невидимого изображения
	//массив информации об изображениях
	const images = [
		{id: 1, range:[0, 3], src: mediaPath + 'main/1.png'},
		{id: 2, range:[3, 7], src: mediaPath + 'main/2.png'},
		{id: 3, range:[7, 17], src: mediaPath + 'main/3.png'},
		{id: 4, range:[17, 26], src: mediaPath + 'main/4.png'},
		{id: 5, range:[26, 41], src: mediaPath + 'main/5.png'},
		{id: 6, range:[41, 51], src: mediaPath + 'main/6.png'},
		{id: 7, range:[51, 61], src: mediaPath + 'main/7.png'},
		{id: 8, range:[61, Infinity], src: mediaPath + 'main/8.png'},
	];

	images.forEach(image => {
		if ((age >= image.range[0] && age < image.range[1]) && imgElements.length > 0) {
			imgElements[0].setAttribute('src', image.src);
			imgElements[0].style.opacity = 1;
			imgElements[0].setAttribute('title', ageSuffix(age));
			imgElements[0].setAttribute('alt', ageSuffix(age));
		}
		// } else {
		// 	imgElements.setAttribute('src', image.src.replace('.png', '-shadow.png'));
		// 	imgElements.style.opacity = opac;
		// }
	});
}
//добавляем склоняемое слово "лет"
function ageSuffix(age) {
	const lastDigit = age % 10;
	const lastTwoDigits = age % 100;
	let suffix;

	// if (lastTwoDigits >= 11)
	switch (lastDigit) {
		case 1:
			suffix = ' год';
			break;
		case 2:
		case 3:
		case 4:
			suffix = ' года';
			break;
		default:
			suffix = ' лет';
			break;
	}
	return "Мне " + age + suffix;
}

document.addEventListener("DOMContentLoaded", (event) => {
	let age = getAge(myAge); // получаем возраст
	const paginatorContainer = document.querySelector('#paginator-container');

	// перебираем все теги img и заменяем путь на нужную фигуру
	trueAge(age);

	// Обработка пагинатора и комментариев
	if (paginatorContainer) {
		paginatorContainer.addEventListener('click', function (event) {
			// Проверяем, является ли кликнутый элемент ссылкой пагинации
			if (event.target.classList.contains('paginator-link')) {
				event.preventDefault(); // Предотвращает переход по ссылке

				const page = event.target.getAttribute('data-page'); // Получаем номер страницы
				const itemId = event.target.getAttribute('data-item-id'); // Получаем item_id

				if (!itemId) {
					// console.error('itemId не найден');
					return; // Прерываем выполнение, если itemId отсутствует
				}

				const timestamp = new Date().getTime();
				const url = `/drawings/drawings/${itemId}/?page=${page}&_=${timestamp}`;
				// console.log(`Запрос к URL: ${url}`);

				fetch(url, {
					headers: {
						'X-Requested-With': 'XMLHttpRequest',
					}
				})
					.then(response => {
						if (!response.ok) {
							throw new Error(`Http ошибка! Статус: ${response.status}`);
						}
						return response.json()
					})
					.then(data => {
						// console.log(data);
						// Обновляем комментарии
						document.querySelector('#comments-container').innerHTML = data.comments_html;
						// Обновляем пагинатор
						document.querySelector('#paginator-container').innerHTML = data.paginator_html;

						bindPaginatorLinks();
					})
					.catch(error => console.error('Error:', error));
			}
		});
	} else {
        console.error('Элемент #paginator-container не найден');
	}
	function bindPaginatorLinks() {
        document.querySelectorAll('.paginator-link').forEach(link => {
            link.addEventListener('click', function(event) {
                // логика для обработки кликов
            });
        });
    }

	const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');
	// console.log(dropdownToggle);
    // console.log(dropdownMenu);

	// console.log("Пытаемся добавить слушатель к dropdownToggle");
	// Код для выпадающего меню
    dropdownToggle.addEventListener('click', function(event) {
		// console.log("Клик на выпадающем меню");
        event.preventDefault(); // Предотвращаем переход по ссылке
        const parentLi = this.parentElement;
        parentLi.classList.toggle('active'); // Переключаем класс 'active'
    });

    // Закрытие выпадающего меню при клике вне его
    document.addEventListener('click', function(event) {
        if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.parentElement.classList.remove('active'); // Убираем класс 'active', если кликнули вне меню
        }
    });
});

