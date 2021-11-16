from django.db import models

class U1FileUpload(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=125)  # Field name made lowercase.
    file_name = models.CharField(db_column='FILE_NAME', max_length=125)  # Field name made lowercase.
    file_upload_name = models.CharField(db_column='FILE_UPLOAD_NAME', max_length=200)  # Field name made lowercase.
    issue_date = models.DateField(db_column='ISSUE_DATE')  # Field name made lowercase.
    expire_date = models.DateField(db_column='EXPIRE_DATE')  # Field name made lowercase.
    entry_date = models.DateField(db_column='ENTRY_DATE')  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=125)  # Field name made lowercase.
    last_update_date = models.DateField(db_column='LAST_UPDATE_DATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U1_FILE_UPLOAD'


class U1Members(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50)  # Field name made lowercase.
    person_id = models.CharField(db_column='PERSON_ID', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=200)  # Field name made lowercase.
    valid_from = models.DateField(db_column='VALID_FROM')  # Field name made lowercase.
    valid_to = models.DateField(db_column='VALID_TO')  # Field name made lowercase.
    last_update_date = models.DateField(db_column='LAST_UPDATE_DATE')  # Field name made lowercase.
    user_level = models.CharField(db_column='USER_LEVEL', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U1_MEMBERS'

class U1CategoryList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=100)  # Field name made lowercase.
    category_desc = models.CharField(db_column='CATEGORY_DESC', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U1_CATEGORY_LIST'



