from utils import detail_view, index_view

def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'drawing', 'creativity/drawings/index.html')

def drawing_detail(request, item_id):
    '''функция вывода детальной информации с комментариями'''
    return detail_view(request, item_id, 'drawing', 'creativity/drawings/drawing.html')