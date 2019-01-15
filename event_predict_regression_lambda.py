"""
Lambda Anomaly Prediction

@author Yang Zeng (zengyang@vmware.com)
"""

import tempfile

import boto3 as boto3
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import model_from_json
from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.preprocessing import image
import os
import sys
import glob
import numpy as np
import json

from avrodefs.Anomaly import Anomaly
from sqs_writer.SQSAnomalyReporter import SQSAnomalyReporter

bucket = 'wavefront-ml-dev'
queue_name = "anomaly-reporting-dev-"
region_name = "us-west-2"
model_key = 'dev/models/regression_model.h5'
json_model_key = 'dev/models/json_model'

W = 1000
H = 100
SLICE = 10
sw = W // SLICE
CUTOFF = 2.0

s3 = boto3.client('s3')
s3c = boto3.resource('s3')

print('downloading model from s3')
s3c.Bucket(bucket).download_file(model_key, '/tmp/model.h5')
s3c.Bucket(bucket).download_file(json_model_key, '/tmp/json_model')

with open('/tmp/json_model', 'r') as json_file:
    json_model = json_file.read()
model = model_from_json(json_model)
model.load_weights('/tmp/model.h5')

def get_files(path):
    if os.path.isdir(path):
        files = glob.glob(os.path.join(path, '*'))
    else:
        files = [path]

    files = [f for f in files if f.endswith('png') and os.stat(f).st_size > 6600]

    if not len(files):
        sys.exit('No images we want to predict on by the given path!')

    return files

def handler(event, context):

    for r in event['Records']:
        #bucket = r['s3']['bucket']['name']
        key = r['s3']['object']['key']

        if '192H' in key or '24H' in key:
            predict(key)

def predict(key):
    tmp = tempfile.NamedTemporaryFile(suffix='.png')
    path = tmp.name
    print('{} : {} : {}'.format(bucket, key, path))
    with open(path, 'wb') as f:
        s3c.Bucket(bucket).download_file(key, path)
        tmp.flush()
    files = get_files(path)

    for f in files:
        img = image.load_img(f, grayscale=True, target_size=(H,W))
        if img is None:
            continue
        x = image.img_to_array(img)
        x = preprocess_input(x, mode='tf')
        x = np.expand_dims(x, axis=0)

        result = []
        anomaly = False

        for k in range(SLICE):
            slice = x[:,:, k * sw:(k + 1) * sw, :]

            pred = model.predict(slice)[0]
            result.append(pred[0])
            if pred >= CUTOFF:
                anomaly = True

        if anomaly:
            report(key)

        with open(path+'_scores.txt', 'w') as f1:
            for i in range(SLICE):
                print(result[i])
                f1.write('   %s ' % (result[i]))
        f1.close()
        dir = os.path.join('output',os.path.dirname(key))
        try:
            s3c.Bucket(bucket).create_bucket(dir)
        except:
            pass
        try:
            s3c.Bucket(bucket).upload_file(path+'_scores.txt', os.path.join('output',key+'_scores.txt'), ExtraArgs={'ContentType':'text/plain','ACL' : 'authenticated-read'})
        finally:
            try:
                os.remove(path+'_scores.txt')
            except:
                pass

def report(path):
    p = path.split("_")
    c = p[0].split("/")
    #    <training/inference>/<cluster>/<customerid>/<dashboard-url>/<4-digit-year>/
    #    <month>/<day-of-month>/T<hour><minute>Z_<training/inference>_section_<chart-section>_row_
    #    <row>_chart_<chart-number-on-row>_<start-time>_<end-time>_params_<params-hash>
    o = s3.get_object(Bucket=bucket, Key=path.replace('.png', '.params.json'))

    q = json.loads(o['Body'].read())
    anomaly = Anomaly(customer=c[2], start_ms=long(p[8])*1000, end_ms=long(p[9])*1000, query_hash=str([s.encode("utf-8") for s in q['_queryList']]),
                      param_hash=q['_paramsHash'],
                      chart_hash=q['_chartHash'], dashboard_id=c[3], section=int(p[3]), row=int(p[5]), col=int(p[7]), model=model_key,
                      image_link='https://s3-'+region_name+'.amazonaws.com/'+bucket + '/'+path,
                      chart_link='',
                      query_params=q['_queryParameters'])
    reporter = SQSAnomalyReporter(queue_name+c[1], region_name=region_name)

    reporter.reportAnomaly(anomaly)

if __name__ == '__main__':
    predict('training/local/collector/integration-system/192H/2018/12/04/T2112Z_training_section_5_row_1_chart_0_1540785153_1541476353_params_-445362456_chartHash_0.png')
