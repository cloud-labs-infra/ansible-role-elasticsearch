./bin/elasticsearch-certutil cert \
                --keep-ca-key \
                --pem \
                --in /tmp/elasticsearch/certs_silent.yml \
                --out /tmp/elasticsearch/test_certs/certs.zip
chmod 777 /tmp/elasticsearch/test_certs/certs.zip