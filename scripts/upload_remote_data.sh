./download_csv_files.sh

../google_appengine/appcfg.py upload_data \
    --email=humitos@gmail.com \
    --config_file=../loaders/$1_loader.py \
    --filename=$1_data.csv \
    --kind=$2 ../ \
    --has_header \
    --log_file=../../bulkloader/`date +%s`.log \
    --db_filename=../../bulkloader/`date +%s`.sql3

./remove_csv_files.sh
