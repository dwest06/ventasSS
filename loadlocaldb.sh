sudo -u postgres dropdb ventassmoke >> /dev/null
sudo -u postgres dropuser ss >> /dev/null
sudo -u postgres createuser ss
sudo -u postgres createdb ventassmoke
sudo -u postgres psql << EOF
alter user ss with password 'smokestormcss';
alter role ss set client_encoding to 'utf8';
alter role ss set default_transaction_isolation to 'read committed';
alter role ss set timezone to 'utc';
grant all privileges on database ventassmoke to ss ;\q
EOF
# alter role SS createdb;