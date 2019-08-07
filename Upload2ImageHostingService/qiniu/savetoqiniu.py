import datetime
from qiniu import Auth, put_file, etag

QINIU_URL = 'http://img.lte.ink/'
# ACCESS_KEY和 SECRET_KEY在七牛云存储的账户信息里可以找到
ACCESS_KEY = ''
SECRET_KEY = ''


def get_current():
    current = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    return current


def upload_to_qiniu(pic):
    """
    将传入的序列化的图片，通过七牛云的接口，上传至bucket，读取接口返回的数据
    :prama: pic: 序列化后的图片
    :return: 结果信息和url的元组
    """
    access = ACCESS_KEY
    secret = SECRET_KEY
    q = Auth(access, secret)
    bucket_name = 'belingud'
    filename = get_current()
    token = q.upload_token(bucket_name, filename)
    loadfile = pic
    ret, info = put_file(token, filename, loadfile)
    if not info.status_code == 200:
        return False, 'upload failed'
    return True, QINIU_URL + ret['key']
