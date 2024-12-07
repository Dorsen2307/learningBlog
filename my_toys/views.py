from utils import detail_view, index_view


def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'toy', 'mytoys/index.html')

def toy_detail(request, item_id):
    return detail_view(request, item_id, 'toy', 'mytoys/toys.html')