FROM ghcr.io/datagutten/duplicati-multimonitor:latest AS static
RUN python /home/app/web/manage.py collectstatic --noinput

FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY --from=static /home/app/static /home/app/static