./download_csv_files.sh

../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=../loaders/$1_loader.py \
    --filename=$1_data.csv \
    --kind=$2 ../ \
    --url=http://localhost:8007/remote_api \
    --has_header \
    --log_file=../../bulkloader/logger.log \
    --db_filename=../../bulkloader/progress.sql3 \
    --batch_size=100

# ./remove_csv_files.sh
