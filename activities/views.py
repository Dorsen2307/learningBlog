from utils import detail_view, index_view


def index(request):
    '''Функция вывода общего контента'''
    return index_view(request, 'activities', 'creativity/activities/index.html')

def activity_detail(request, item_id):
    return detail_view(request, item_id, 'activities', 'creativity/activities/activity.html')
