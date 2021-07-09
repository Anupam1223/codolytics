FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

# COPY fullchain.pem /etc/letsencrypt/live/api.codolytics.com/fullchain.pem
# COPY privkey.pem /etc/letsencrypt/live/api.codolytics.com/privkey.pem
# COPY options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
# COPY ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem