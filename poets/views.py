from utils import detail_view, index_view

def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'poets', 'creativity/poets/index.html')

def poet_detail(request, item_id):
    return detail_view(request, item_id, 'poets', 'creativity/poets/poet.html')