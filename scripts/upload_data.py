import os
import glob
import sys

kinds = {
    'busstop': 'BusStop',
    'bustime': 'BusTime',
    'news': 'News',
    'busdirection': 'BusDirection',
}

remote = '--remote' in sys.argv

if remote == True:
    cmd = '''../../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=%s \
    --filename=%s \
    --kind=%s ../ \
    --has_header \
    --log_file=../../bulkloader/logger.log \
    --db_filename=../../bulkloader/%s.sql3 \
    --batch_size=5
'''
else:
    cmd = '''../../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=%s \
    --filename=%s \
    --kind=%s ../ \
    --url=http://localhost:8007/remote_api \
    --has_header \
    --log_file=../../bulkloader/logger.log \
    --db_filename=../../bulkloader/%s.sql3 \
    --batch_size=100
'''

for filename in sorted(glob.glob('../fixtures/*.csv')):
    csv_filename = filename
    filename = os.path.basename(filename)

    name = filename.split('_')[0]
    if remote:
        sql = 'remote_%s' % filename.split('.')[0]
    else:
        sql = filename.split('.')[0]
    kind = kinds[name]
    config_file = '../loaders/%s_loader.py' % name
    new_cmd = cmd % (config_file, csv_filename, kind, sql)
    print new_cmd
    os.system(new_cmd)
