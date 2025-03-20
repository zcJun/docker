FROM nginx:latest

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /var/www/html/project

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
