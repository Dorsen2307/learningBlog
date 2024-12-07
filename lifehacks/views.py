from utils import detail_view, index_view

def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'lifehack', 'creativity/lifehacks/index.html')

def lifehack_detail(request, item_id):
    return detail_view(request, item_id, 'lifehack', 'creativity/lifehacks/lifehack.html')