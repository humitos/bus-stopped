./download_csv_files.sh

# The order of the uploading process IS IMPORTANT

# NEWS
../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=../loaders/news_loader.py \
    --filename=news_data.csv \
    --kind=News ../ \
    --url=http://localhost:8007/remote_api \
    --has_header \
    --log_file=../../bulkloader/`date +%s`.log \
    --db_filename=../../bulkloader/`date +%s`.sql3 \
    --batch_size=100

# BUS STOP
../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=../loaders/busstop_loader.py \
    --filename=busstop_data.csv \
    --kind=BusStop ../ \
    --url=http://localhost:8007/remote_api \
    --has_header \
    --log_file=../../bulkloader/`date +%s`.log \
    --db_filename=../../bulkloader/`date +%s`.sql3 \
    --batch_size=100

# BUS TIME
../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=../loaders/bustime_loader.py \
    --filename=bustime_data.csv \
    --kind=BusTime ../ \
    --url=http://localhost:8007/remote_api \
    --has_header \
    --log_file=../../bulkloader/`date +%s`.log \
    --db_filename=../../bulkloader/`date +%s`.sql3 \
    --batch_size=100
