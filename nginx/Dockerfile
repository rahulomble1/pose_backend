FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY physio_flask_backend/nginx/nginx.conf /etc/nginx/conf.d/

COPY ./elitefitforyou_ssl/elitefitforyou.com.crt /etc/nginx/

COPY ./elitefitforyou_ssl/elitefitforyou.com.key /etc/nginx/

CMD ["nginx", "-g", "daemon off;"]
