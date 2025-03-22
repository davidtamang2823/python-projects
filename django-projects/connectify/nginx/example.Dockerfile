FROM nginx:1.25.2

RUN rm ./etc/nginx/conf.d/default.conf

COPY ./nginx/nginx-local.conf ./etc/nginx/conf.d/nginx-local.conf
