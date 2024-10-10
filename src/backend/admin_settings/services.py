import io
import re
import boto3
import zipfile
import logging
import random, string, requests

from django.conf import settings
from django.contrib.auth import get_user_model
from botocore.exceptions import ClientError
from ..accounts.serializers import UserSerializer
from ..base.utils.email import send_from_template
from decouple import config


def delete_child(parent_id, model_class):
    children = []
    if model_class.objects.filter(parent=parent_id, is_active=True).exists():
        query = model_class.objects.filter(parent=parent_id)
        for one in query:
            children.append(one.pk)
            delete_child(one.pk, model_class)
            one.is_active = False
            one.save()
        return children
    else:
        return children


def dropdown_tree(settings_list, serializer_class, model_class, parent_id=None, path=""):
    separator = "$#$"
    if len(settings_list) == 0:
        return []
    else:
        data = []
        for i in range(len(settings_list)):
            child = {
                **settings_list[i],
                'parent': parent_id,
                'path': path + separator + settings_list[i]['title'] if path else settings_list[i]['title'],
                'value': settings_list[i]['title'] + "-" + str(parent_id) if 'title' in settings_list[i] else ""
            }
            if len(child['children']) > 0:
                children = child['children']
                child['children'] = []
                queryset = model_class.objects.filter(name=child['title'], is_active=True)
                if parent_id:
                    queryset = queryset.filter(parent=parent_id)
                for item in queryset:
                    item_path = path + separator + child['path'] + separator + item.value if path else \
                        child['path'] + separator + item.value
                    child['children'].append({
                        'id': item.id,
                        'title': item.value,
                        'value': item.value + "-" + str(parent_id),
                        'path': item_path.split(separator),
                        'disabled': True,
                        'children': dropdown_tree(children, serializer_class, model_class, item.id, item_path)
                    })
            child['path'] = child['path'].split(separator)
            data.append(child)
        data.sort(key=lambda x: x.get('title'))
        return data


def generate_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def remove_special_characters(sting):
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', sting)


def generate_username(first_name=None, middle_name=None, last_name=None):
    first_name = first_name.replace(" ", "").replace(".", "") if first_name else first_name
    middle_name = middle_name.replace(" ", "").replace(".", "") if middle_name else middle_name
    last_name = last_name.replace(" ", "").replace(".", "") if last_name else last_name
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    if first_name:
        first_name = remove_special_characters(first_name)
        if len(first_name) > 4:
            return first_name[0:4].upper() + random_string
        if middle_name:
            middle_name = first_name + remove_special_characters(middle_name)
            if len(middle_name) > 4:
                return middle_name[0:4].upper() + random_string
        else:
            middle_name = ''
        if last_name:
            last_name = first_name + middle_name + remove_special_characters(last_name)
            if len(last_name) > 4:
                return last_name[0:4].upper() + random_string
        return first_name.upper() + random_string
    return None


def create_presigned_url(object_name, file_type):
    s3_client = boto3.client('s3', settings.AWS_S3_REGION_NAME,
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    try:
        response = s3_client.generate_presigned_url('put_object', Params={
            'Bucket': settings.AWS_STORAGE_TEMP_BUCKET_NAME,
            'Key': object_name,
            'ContentType': file_type})
    except ClientError as e:
        logging.error(e)
        return None
    return response


def s3_upload_file_from_local(file_path, destination):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_client.upload_file(file_path, settings.AWS_STORAGE_TEMP_BUCKET_NAME, destination)
        return True
    except ClientError as e:
        print(f"An error occurred: {e}")
        return False


def create_update_s3_record(from_path=None, to_path=None, path='common', is_onboard=False):
    buket_name = settings.AWS_STORAGE_ONBOARD_BUCKET_NAME if is_onboard else settings.AWS_STORAGE_BUCKET_NAME
    s3_client = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    s3 = s3_client.resource('s3')
    if from_path == to_path:
        return None, from_path
    if from_path:
        try:
            s3.Object(buket_name, from_path).delete()
        except:
            pass
    if to_path:
        try:
            copy_source = {'Bucket': settings.AWS_STORAGE_TEMP_BUCKET_NAME, 'Key': 'temp/' + to_path}
            target_bucket = s3.Bucket(buket_name)
            file_name = to_path.split('/')[-1]
            destination_path = '{path}{image}'.format(path=path, image=file_name)
            target_bucket.copy(copy_source, destination_path)
            file_path = destination_path
            s3.Object(settings.AWS_STORAGE_TEMP_BUCKET_NAME, 'temp/' + to_path).delete()
            size_response = s3.Object(buket_name, destination_path)
            file_size = size_response.content_length
            return file_size, file_path
        except Exception as e:
            print(e)
            pass
        return None, to_path
    return None, None


def s3_move_files(from_path, to_path):
    s3_client = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3 = s3_client.client('s3')
    source_bucket = settings.AWS_STORAGE_BUCKET_NAME
    # List objects with the specified prefix
    source_objects = s3.list_objects_v2(Bucket=source_bucket, Prefix=from_path)
    for obj in source_objects.get('Contents', []):
        source_key = obj['Key']
        target_key = source_key.replace(from_path, to_path, 1)  # Replace the prefix
        # Copy each object to the new destination
        s3.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Bucket=source_bucket,
            Key=target_key
        )
        # Delete the original object
        s3.delete_object(Bucket=source_bucket, Key=source_key)
    return None


def create_update_s3_directory(from_path=None, to_path=None, path='common'):
    s3_client = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    s3 = s3_client.resource('s3')
    if from_path:
        try:
            bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
            bucket.objects.filter(Prefix=from_path).delete()
        except:
            pass
    if to_path:
        try:
            final_path = path + to_path + "/"
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=(final_path))
            return final_path
        except:
            pass
    return None


def get_presigned_url(object_name, expiration=config('PRESIGNED_EXPIRY_SECONDS', cast=int), is_onboard=False):
    s3_client = boto3.client('s3', settings.AWS_S3_REGION_NAME,
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    try:
        bucket_name = settings.AWS_STORAGE_ONBOARD_BUCKET_NAME if is_onboard else settings.AWS_STORAGE_BUCKET_NAME
        response = s3_client.generate_presigned_url('get_object', ExpiresIn=expiration,
                                                    Params={'Bucket': bucket_name, 'Key': object_name})
    except ClientError as e:
        logging.error(e)
        return None
    response = response.split('.com/') if response else None
    return response[1] if response else ""


def employee_photo_path(court_id):
    if court_id:
        return "COURT_" + str(court_id) + '/' + 'employee_photos/'
    raise ValueError('invalid employee_photo_path')


def customer_photo_path(court_id):
    if court_id:
        return "COURT_" + str(court_id) + '/' + 'customer_photos/'
    raise ValueError('invalid customer_photo_path')


def support_path():
    return "SUPPORT/"


def ticket_path():
    return "TICKET_MEDIA/"


def qr_code_path():
    return "QR_CODES/"


def zip_s3_folder(file_name, file_path, zip_path='downloads/'):
    s3_client = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    s3 = s3_client.client('s3')
    buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            infile_object = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=file_path)['Contents']
            for file_path in infile_object:
                response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path['Key'])
                file_content = response['Body'].read()
                zip_file.writestr(file_path['Key'].split('/')[-1], file_content)
        buffer.seek(0)
        s3.upload_fileobj(buffer, settings.AWS_STORAGE_BUCKET_NAME, zip_path + file_name)
        return get_presigned_url(zip_path + file_name)
    except:
        return None


def s3_copy_record(source=None, folder_path='temp/ORDER/'):
    s3_client = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, )
    s3 = s3_client.resource('s3')
    try:
        copy_source = {'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': source}
        target_bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        file_name = source.split('/')[-1]
        destination_path = '{path}{image}'.format(path=folder_path, image=file_name)
        target_bucket.copy(copy_source, destination_path)
    except:
        pass


def create_new_user(first_name=None, middle_name=None, last_name=None, email=None, mobile=None,
                    username=None, password=None, dob=None):
    user = get_user_model().objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                           email=email, mobile=mobile, username=username, dob=dob)
    password = generate_password() if not password else password
    user.set_password(password)
    user.save()
    return user, password


def create_employee(email=None, name=None, mobile=None):
    user = get_user_model().objects.filter(email=email, is_active=True).first()
    if not user:
        user, password = create_new_user(email=email, first_name=name, mobile=mobile)
        template = "employee_added.html"
        subject = "Your profile is added to a new Publisher"
        data = {
            'data': UserSerializer(user).data,
        }
        if password:
            subject = "Your profile has been created"
            template = "user_created.html"
            data['password'] = password
        send_from_template(user.email, subject, template, data)
    return user
