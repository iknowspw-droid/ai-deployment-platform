# ==========================================
# Production Web Server Layer
# ==========================================
FROM nginx:1.25-alpine

# Remove default boilerplate configurations provided by Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copy a custom, hardened Nginx configuration file into place
COPY nginx.conf /etc/nginx/conf.d/

# Copy our actual static web code bundle into Nginx's default public hosting directory
COPY index.html /usr/share/nginx/html/

EXPOSE 80

# Run Nginx in the foreground so the Docker container remains active
CMD ["nginx", "-g", "daemon off;"]
