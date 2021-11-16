from datetime import date
from django.db import connections
from .models import U1Members
from .encryption_utility import *

def get_active_status_list():
    active_status = [
        (None, 'Select Active Status....'),
        ('1', 'Active'),
        ('0', 'Inactive'),

    ]
    # category = ['option1', 'option2', 'option3']
    # choices = [tuple([each, each]) for each in category]
    return active_status

def get_user_level_list():
    user_level = [
        (None, 'Select User Level....'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    # category = ['option1', 'option2', 'option3']
    # choices = [tuple([each, each]) for each in category]
    return user_level

def get_all_user():
    get_all_user_query = "select ROW_NUMBER() OVER(ORDER BY c.user_id) AS row_no, * from U1_MEMBERS as c"
    user = U1Members.objects.raw(get_all_user_query)
    return user

def get_user_by_email(user_email):
    get_user_by_email_query = "select * from U1_MEMBERS where " \
                           "email='" + user_email.strip() + "' "
    user = U1Members.objects.raw(get_user_by_email_query)
    return user

def get_user_by_id(user_id):
    get_user_by_email_query = "select * from U1_MEMBERS where " \
                           "user_id='" + user_id.strip() + "' "
    user = U1Members.objects.raw(get_user_by_email_query)
    return user

def get_user_by_person_id(person_id):
    get_user_by_email_query = "select * from U1_MEMBERS where " \
                           "person_id='" + person_id.strip() + "' "
    user = U1Members.objects.raw(get_user_by_email_query)
    return user

def add_user_to_db(form_data, valid_from, valid_to):
    try:
        user_id = str(form_data.get('user_id').strip())
        user_name = str(form_data.get('user_name').strip())
        person_id = str(form_data.get('person_id').strip())
        user_email = str(form_data.get('user_email').strip())
        active_status = str(form_data.get('active_status'))
        created_at = str(date.today().strftime('%Y-%m-%d'))
        user_level = str(form_data.get('user_level'))
        valid_from = str(valid_from)
        valid_to = str(valid_to)
        password = str(encrypt(form_data.get('user_pass')))
        cursor = connections['default'].cursor()
        insert_query = "insert into U1_MEMBERS([USER_ID],[NAME],[PERSON_ID],[EMAIL],[STATUS],[PASSWORD],[VALID_FROM],[VALID_TO]," \
                       "[LAST_UPDATE_DATE],[USER_LEVEL]) VALUES ('"+user_id+"','"+user_name+"','"+person_id+"','"+user_email+"" \
                       "',"+active_status+",'"+password+"','"+valid_from+"','"+valid_to+"','"+created_at+"','"+user_level+"') "
        cursor.execute(insert_query)
        return True
    except:
        return False
def update_user(form_data, user_id):
    try:
        name = str(form_data.get('user_name').strip())
        email = str(form_data.get('user_email').strip())
        status = str(form_data.get('active_status'))
        user_level = str(form_data.get('user_level'))
        updated_at = str(date.today().strftime('%Y-%m-%d'))
        cursor = connections['default'].cursor()
        insert_query = "update U1_MEMBERS set NAME='"+name+"',EMAIL='"+email+"',STATUS="+status+",USER_LEVEL=" \
                        "'"+user_level+"', LAST_UPDATE_DATE='"+updated_at+"' where user_id='"+user_id+"'"
        cursor.execute(insert_query)
        return True
    except:
        return False

def change_password(user_id, password):
    password = str(encrypt(password))
    cursor = connections['default'].cursor()
    password_update_query = "update U1_MEMBERS set password='"+password+"' where user_id='"+user_id+"'"
    cursor.execute(password_update_query)