from django.http import HttpResponse, Http404, HttpResponse
from django.template import loader
from .forms import *
from django.shortcuts import render


def index(request):
    try:
        template = loader.get_template('portal/index.html')
        try:
            context = {
                'session_user_email': request.session.get('user_email', None)
            }
        except:
            context = {
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    return HttpResponse(template.render(context, request))


def login(request):
    try:
        template = loader.get_template('portal/login.html')
        context = {
            'form': LoginForm(),
        }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    return HttpResponse(template.render(context, request))

def uploadFile(request):
    try:
        if request.method == 'POST':
            # file_name = request.POST.getlist('file_name')
            form = uploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_upload = request.FILES.getlist('file_upload')
                for each in file_upload:
                    handle_uploaded_file(each)
                template = loader.get_template('portal/uploadfile.html')
                context = {
                    'form': uploadForm(),
                    'confirmation_message': 'Upload completed!',
                }
            else:
                template = loader.get_template('portal/uploadfile.html')
                context = {
                    'form': uploadForm(),
                    'denial_message': 'Upload not completed!',
                }
        else:
            template = loader.get_template('portal/uploadfile.html')
            context = {
                'form': uploadForm(),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    return HttpResponse(template.render(context, request))