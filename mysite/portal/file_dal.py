import os
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
    with open('static/file_upload/'+f.name, 'wb+') as destination:
        # if destination.read(f.name):
        #     print(f.name)
        # else:
            for chunk in f.chunks():
                destination.write(chunk)