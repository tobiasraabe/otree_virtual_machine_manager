# -*- coding: utf-8 -*-

NGINX_CONF = """
map $http_upgrade $connection_upgrade { # Some variables for configuring the protocol switch
        default upgrade;
        ''      close;
    }

server {
    listen SSLPORT ssl ;
    listen [::]:SSLPORT ssl ;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';

# create your own ssl certification using e.g. letsencrypt (installed on system)
    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    add_header Strict_Transport-Secutiry max-age=31536000;
    #ssl_dhparm /etc/nginx/ssl/dhparm.pem;
    ssl_session_cache shared:ssl_session_cache:10m;

    root /home/otree-admin/otree_project;
    index index.html index.htm index.nginx-debian.html;

    server_name _;
    location ^~ /_static/  {
            root OTREEHOME;
            include /etc/nginx/mime.types;
        }
    location = /favico.ico  {
            root /app/favico.ico;
        }
    location / {
            proxy_pass http://127.0.0.1:DAPHNEPORT;
            proxy_http_version 1.1; # protocol switch needed
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade; # End of the configuration for oTree
            proxy_set_header HOST $host:HTTPPORT;
            proxy_set_header X-Real-Ip $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
    }
}

server {
    listen HTTPPORT;
    server_name _;
    return 301 https://$host:SSLPORT$request_uri;
}
"""
