import os
from django.db import connections
from datetime import date
from .models import *
from django.http import FileResponse
import reportlab


def get_category_list():
    # category = [
    #     (None, 'Select a country....'),
    #     ('option1', 'option1'),
    #     ('option2', 'option2'),
    #     ('option3', 'option3'),
    #     ('option3', 'option3'),
    # ]
    category = []
    get_details_query = "select * from U1_CATEGORY_LIST"
    category_list = U1CategoryList.objects.raw(get_details_query)
    for each in category_list:
        category.append(each.category)
    # category = ['option1', 'option2', 'option3']
    # choices = [tuple([each, each]) for each in category]
    choices = [(None, 'Select a category...')]
    [choices.append([each, each]) for each in category]
    return choices

def get_category():
    category = []
    get_details_query = "select * from U1_CATEGORY_LIST"
    category_list = U1CategoryList.objects.raw(get_details_query)
    for each in category_list:
        category.append(each.category)
    # category = ['option1', 'option2', 'option3']
    return category


def handle_uploaded_file(f):
    if os.path.isfile('static/file_upload/' + f.name):
        import glob
        try:
            fileCounter = \
                glob.glob1('static/file_upload/', f.name.split('.')[0] + "_[0-9]*")[-1].split('.')[0].split('_')[-1]
            fileCounter = int(fileCounter) + 1
        except:
            fileCounter = 0
        with open('static/file_upload/' + f.name.split('.')[0] + "_" + str(fileCounter) + "." + f.name.split('.')[1],
                  'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            return str(f.name.split('.')[0] + "_" + str(fileCounter) + "." + f.name.split('.')[1])
    else:
        with open('static/file_upload/' + f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            return str(f.name)


def upload_to_db(file_name_list, category_list, issue_date_list, expire_date_list, file_upload_list,user_id):
    try:
        for each in range(0, len(file_name_list)):
            created_at = date.today().strftime('%d-%m-%Y')
            file_upload_name = handle_uploaded_file(file_upload_list[each])
            cursor = connections['default'].cursor()
            insert_query = "insert into U1_FILE_UPLOAD(category,file_name,file_upload_name,issue_date,expire_date,entry_date,user_id," \
            "last_update_date) values('" + str(category_list[each]) + "','" + str(file_name_list[each]) + "','" + str(file_upload_name) + "','" + issue_date_list[each] \
            + "','" + expire_date_list[each] + "','" + created_at + "','" + str(user_id) + "','" + created_at + "')"
            cursor.execute(insert_query)
        return True
    except:
        return False


def get_all_files_db():
    get_details_query = " select ROW_NUMBER() OVER(ORDER BY c.ID) AS row_no, * from U1_FILE_UPLOAD as c"
    file_details = U1FileUpload.objects.raw(get_details_query)
    return file_details


def get_category_files_db(category):
    get_details_query = " select ROW_NUMBER() OVER(ORDER BY c.ID) AS row_no, * " \
                        "from U1_FILE_UPLOAD as c where category='"+category+"'"
    category_file_details = U1FileUpload.objects.raw(get_details_query)
    return category_file_details


def get_category_file_count():
     get_details_query = 'select ROW_NUMBER() OVER(ORDER BY cat.category) AS ID, cat.category, ' \
                         'count(fu.category) as category_count from U1_CATEGORY_LIST cat left outer join ' \
                         'U1_FILE_UPLOAD fu on cat.CATEGORY= fu.CATEGORY group by cat.category'
     category_file_count = U1CategoryList.objects.raw(get_details_query)
     return category_file_count