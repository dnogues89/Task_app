# Use the official Alpine Nginx image
FROM nginx:alpine

# Install Certbot
RUN apk add --no-cache certbot python3 py3-pip openssl \
    && pip3 install 'cryptography' 'pyOpenSSL'

# Expose ports 80 and 8080
EXPOSE 80 8080

