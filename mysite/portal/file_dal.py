import os
import time
import uuid
from django.core.exceptions import ValidationError

def get_category_list():
    # category = [
    #     (None, 'Select a country....'),
    #     ('option1', 'option1'),
    #     ('option2', 'option2'),
    #     ('option3', 'option3'),
    #     ('option3', 'option3'),
    # ]
    category = ['option1', 'option2', 'option3']
    choices = [tuple([each, each]) for each in category]
    return choices


def handle_uploaded_file(f):
    with open('static/file_upload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

        filename = os.path.join(f.name, '')


# def handle_uploaded_file(f):
#         if os.path.isfile('static/file_upload/'+f.name):
#
#             rename_file = f.name.split('.')[0]+"_"+str(time.time())+f.name.split('.')[1]
#             filename = os.path.join(f.name, '')
#             filename = os.(f.name, rename_file)
#             if os.path.isfile('static/file_upload/'+filename):
#                 handle_uploaded_file(filename)
#             with open('static/file_upload/'+filename, 'wb+') as destination:
#                 for chunk in filename.chunks():
#                     destination.write(chunk)
#                 destination.close()
#                 print(f.name)
#         else:
#             for chunk in f.chunks():
#                 with open('static/file_upload/' + f.name, 'wb+') as destination:
#                     for chunk in f.chunks():
#                         destination.write(chunk)
#                     destination.close()