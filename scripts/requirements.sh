wget \
    -c http://googleappengine.googlecode.com/files/google_appengine_1.4.2.zip \
    -O ../google_appengine_1.4.2.zip
cd ..
unzip google_appengine_1.4.2.zip
ln -s google_appengine/appcfg.py .
ln -s google_appengine/dev_appserver.py

