from django.template.response import TemplateResponse

def index2(request):
    return TemplateResponse(request, 'index2.html', {
            'var1': 'This is var1',
            'var2': 'This is var2',
            'list_var': ['sun', 'sol', 'soleil'],
            'var3': 55 + 35 / 10,
    })
