from django.shortcuts import render_to_response


def pag_not_found(request, exception):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

def no_access(request, exception):
    # 全局403处理函数
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response
