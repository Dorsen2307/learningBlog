from utils import detail_view, index_view

def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'drawings', 'creativity/drawings/index.html')

def drawing_detail(request, item_id):
    '''функция вывода детальной информации с комментариями'''
    return detail_view(request, item_id, 'drawings', 'creativity/drawings/drawing.html')