from utils import detail_view, index_view

def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'craft', 'creativity/crafts/index.html')

def craft_detail(request, item_id):
    return detail_view(request, item_id, 'craft', 'creativity/crafts/craft.html')