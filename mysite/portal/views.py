from django.http import HttpResponse, Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import *
from django.http import FileResponse
from .account_dal import *


def index(request):
    try:
        template = loader.get_template('portal/index.html')
        try:
            context = {
                'session_user_name': request.session.get('user_name', None),
                'session_user_id': request.session.get('user_id', None),
                'session_user_pass': request.session.get('user_pass', None),
                'session_user_level': request.session.get('user_level', None),
                'categories': get_category(),
                'category_file_count' : get_category_file_count(),
            }
        except:
            context = {
                'categories': get_category(),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    return HttpResponse(template.render(context, request))


def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                request.session.modified = True
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(30*60)
                user_detail = get_user_by_id(form.cleaned_data.get('user_id'))
                for detail in user_detail:
                    request.session['user_name'] = detail.name
                    request.session['user_id'] = detail.user_id
                    request.session['user_pass'] = detail.password
                    request.session['user_level'] = detail.user_level
                    return HttpResponseRedirect('/')
            elif form.has_error('user_id', code=None):
                for error in form.errors['user_id']:
                    user_id_error = error
                    context = {
                        'form': form,
                        'user_id_error': user_id_error,
                        'denial_message': 'Login attempt fail!',
                    }
            elif form.has_error('user_pass', code=None):
                for error in form.errors['user_pass']:
                    pass_error = error
                context = {
                    'form': form,
                    'pass_error': pass_error,
                    'denial_message': 'Login attempt fail!',
                }
        else:
            context = {
                'form': LoginForm(),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/login.html')
    return HttpResponse(template.render(context, request))

def logout(request):
    try:
        request.session.modified = True
        if request.session['user_id']:
            del request.session['user_name']
            del request.session['user_id']
            del request.session['user_level']
            del request.session['user_pass']
        return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')

def changePassword(request):
    try:
        if request.method == 'POST':
            user_id = request.session.get('user_id', None)
            form = ChangePassForm(request.POST, user_id = user_id)
            if form.is_valid():
                form_data = form.cleaned_data
                change_password(user_id, form_data.get('conf_pass'))
                context = {
                    'form': form,
                    'session_user_name': request.session.get('user_name', None),
                    'session_user_id': request.session.get('user_id', None),
                    'session_user_pass': request.session.get('user_pass', None),
                    'session_user_level': request.session.get('user_level', None),
                    'confirmation_message': 'Password Changed!',
                }
            elif form.has_error('old_pass', code=None):
                for error in form.errors['old_pass']:
                    old_pass_error = error
                    context = {
                        'form': form,
                        'old_pass_error': old_pass_error,
                        'denial_message': 'Change password attempt fail!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            elif form.has_error('conf_pass', code=None):
                for error in form.errors['conf_pass']:
                    conf_pass_error = error
                context = {
                    'form': form,
                    'conf_pass_error': conf_pass_error,
                    'denial_message': 'Change password attempt fail!',
                    'session_user_name': request.session.get('user_name', None),
                    'session_user_id': request.session.get('user_id', None),
                    'session_user_pass': request.session.get('user_pass', None),
                    'session_user_level': request.session.get('user_level', None),
                }
        else:
            context = {
                'form': ChangePassForm(),
                'session_user_name': request.session.get('user_name', None),
                'session_user_id': request.session.get('user_id', None),
                'session_user_pass': request.session.get('user_pass', None),
                'session_user_level': request.session.get('user_level', None),
            }
    except Exception as error:
        raise error
    template = loader.get_template('portal/changepassword.html')
    return HttpResponse(template.render(context, request))

def addUser(request):
    try:
        if request.method == 'POST':
            form = adduserForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                insert_info = add_user_to_db(form_data, request.POST.get('valid_from'), request.POST.get('valid_to'))
                if insert_info:
                    context = {
                        'form': adduserForm(),
                        'confirmation_message': 'User entry successful!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
                else:
                    context = {
                        'form': form,
                        'denial_message': 'ERROR IN DATABASE!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            elif form.has_error('user_id', code=None):
                for error in form.errors['user_id']:
                    user_id_error = error
                    context = {
                        'form': form,
                        'user_id_error': user_id_error,
                        'denial_message': 'User entry unsuccessful!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            elif form.has_error('person_id', code=None):
                for error in form.errors['person_id']:
                    person_id_error = error
                    context = {
                        'form': form,
                        'person_id_error': person_id_error,
                        'denial_message': 'User entry added!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            else:
                context = {
                    'session_user_name': request.session.get('user_name', None),
                    'session_user_id': request.session.get('user_id', None),
                    'session_user_pass': request.session.get('user_pass', None),
                    'session_user_level': request.session.get('user_level', None),
                    'form': form,
                }
        else:
            context = {
                'session_user_name': request.session.get('user_name', None),
                'session_user_id': request.session.get('user_id', None),
                'session_user_pass': request.session.get('user_pass', None),
                'session_user_level': request.session.get('user_level', None),
                'form': adduserForm(),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/adduser.html')
    return HttpResponse(template.render(context, request))

def uploadFile(request):
    try:
        if request.method == 'POST':
            # file_name = request.POST.getlist('file_name')
            form = uploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_name_list = request.POST.getlist('file_name')
                category_list = request.POST.getlist('category')
                issue_date_list = request.POST.getlist('issue_date')
                expire_date_list = request.POST.getlist('expire_date')
                file_upload_list = request.FILES.getlist('file_upload')
                user_id = request.session.get('user_id', None)
                insert_info = upload_to_db(file_name_list, category_list, issue_date_list, expire_date_list, file_upload_list, user_id)
                if insert_info:
                    context = {
                        'form': form,
                        'confirmation_message': 'Upload completed successfully!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
                else:
                    context = {
                        'form': form,
                        'denial_message': 'ERROR IN DATABASE!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            else:
                context = {
                    'form': form,
                    'denial_message': 'Upload unsuccessful!',
                    'session_user_name': request.session.get('user_name', None),
                    'session_user_id': request.session.get('user_id', None),
                    'session_user_pass': request.session.get('user_pass', None),
                    'session_user_level': request.session.get('user_level', None),
                }
        else:
            context = {
                'form': uploadForm(),
                'session_user_name': request.session.get('user_name', None),
                'session_user_id': request.session.get('user_id', None),
                'session_user_pass': request.session.get('user_pass', None),
                'session_user_level': request.session.get('user_level', None),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/uploadfile.html')
    return HttpResponse(template.render(context, request))

def viewFile(request):
    try:
        context = {
            'file_details' : get_all_files_db(),
            'session_user_name': request.session.get('user_name', None),
            'session_user_id': request.session.get('user_id', None),
            'session_user_pass': request.session.get('user_pass', None),
            'session_user_level': request.session.get('user_level', None),
        }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/viewfile.html')
    return HttpResponse(template.render(context, request))

def viewCategoryFile(request, category):
    try:
        context = {
            'category': category,
            'category_file_details' : get_category_files_db(category),
            'session_user_name': request.session.get('user_name', None),
            'session_user_id': request.session.get('user_id', None),
            'session_user_pass': request.session.get('user_pass', None),
            'session_user_level': request.session.get('user_level', None),
        }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/viewcategory.html')
    return HttpResponse(template.render(context, request))

def viewUser(request):
    try:
        context = {
            'user_details' : get_all_user(),
            'session_user_name': request.session.get('user_name', None),
            'session_user_id': request.session.get('user_id', None),
            'session_user_pass': request.session.get('user_pass', None),
            'session_user_level': request.session.get('user_level', None),
        }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/viewuser.html')
    return HttpResponse(template.render(context, request))

def editUser(request, user_id):
    try:
        user = get_user_by_id(user_id)
        for detail in user:
            user_name = detail.name
            person_id = detail.person_id
            user_email = detail.email
            user_level = detail.user_level
            active_status = detail.status
        form = edituserForm()
        form.fields['user_id'].initial = user_id
        form.fields['person_id'].initial = person_id
        form.fields['user_name'].initial = user_name
        form.fields['user_email'].initial = user_email
        form.fields['user_level'].initial = user_level
        form.fields['active_status'].initial = active_status
        if request.method == 'POST':
            form = edituserForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                insert_info = update_user(form_data,user_id)
                user = get_user_by_id(user_id)
                for detail in user:
                    user_name = detail.name
                    person_id = detail.person_id
                    user_email = detail.email
                    user_level = detail.user_level
                    active_status = detail.status
                form.fields['user_id'].initial = user_id
                form.fields['person_id'].initial = person_id
                form.fields['user_name'].initial = user_name
                form.fields['user_email'].initial = user_email
                form.fields['user_level'].initial = user_level
                form.fields['active_status'].initial = active_status
                if insert_info:
                    context = {
                        'user_id': user_id,
                        'form': form,
                        'confirmation_message': 'User updated successfully!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
                else:
                    context = {
                        'user_id': user_id,
                        'form': form,
                        'denial_message': 'ERROR IN DATABASE!',
                        'session_user_name': request.session.get('user_name', None),
                        'session_user_id': request.session.get('user_id', None),
                        'session_user_pass': request.session.get('user_pass', None),
                        'session_user_level': request.session.get('user_level', None),
                    }
            else:
                context = {
                    'user_id': user_id,
                    'form': form,
                    'denial_message': 'Update unsuccessful!',
                    'session_user_name': request.session.get('user_name', None),
                    'session_user_id': request.session.get('user_id', None),
                    'session_user_pass': request.session.get('user_pass', None),
                    'session_user_level': request.session.get('user_level', None),
                }
        else:
            context = {
                'user_id': user_id,
                'form' : form,
                'session_user_name': request.session.get('user_name', None),
                'session_user_id': request.session.get('user_id', None),
                'session_user_pass': request.session.get('user_pass', None),
                'session_user_level': request.session.get('user_level', None),
            }
    except Exception as error:
        raise error
        # raise Http404("Page does not exist")
    template = loader.get_template('portal/edituser.html')
    return HttpResponse(template.render(context, request))

SCOPES = ['https://www.googleapis.com/auth/documents']

def openPDF(request, file_name):
    buffer = open('static/file_upload/' + file_name, 'rb')
    return FileResponse(buffer, as_attachment=False, filename=file_name, content_type='application/pdf')

def openImage(request, file_name):
    buffer = open('static/file_upload/' + file_name, 'rb')
    return FileResponse(buffer, as_attachment=False, filename=file_name, content_type='image/png')

def openDoc(request, file_name):
    buffer = open('static/file_upload/' + file_name, 'rb')
    return FileResponse(buffer, as_attachment=False, filename=file_name, content_type='application/ms-word')

def downloadFile(request, file_name):
    buffer = open('static/file_upload/' + file_name, 'rb')
    return FileResponse(buffer, as_attachment=True, filename=file_name)