# NGINX

### A simple example
The following configuration serves a static file from the specified directory when accessed via the given IP address.

```nginx
server {
    listen 80;
    server_name 192.168.1.190;

    root /var/www/my_site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

- **listen 80;**: The server listens for incoming requests on port 80.
- **server_name 192.168.1.190;**: This specifies the server's name or IP address that it responds to.
- **root /var/www/my_site;**: The root directory for serving files is set to `/var/www/my_site`.
- **index index.html;**: The default file to serve when accessing the root directory is `index.html`.
- **location / { ... }**: This block handles requests for the root URL.
  - **try_files $uri $uri/ =404;**: It attempts to serve the requested file (`$uri`) or directory (`$uri/`). If neither exists, it returns a 404 error.


### another example
```nginx
server {
    listen 80;
    server_name 192.168.1.190;

    location /files/ {
        alias /var/www/my_site/files/;
        autoindex on;
        autoindex_exact_size off;  # Optional
        autoindex_localtime on;    # Optional
    }
}
```
This configuration allows users to browse and view files located in `/var/www/my_site/files/` through the web server.

- **location /files/**: This block applies to requests that start with `/files/`.
- **alias /var/www/my_site/files/**: It maps the `/files/` URL to the filesystem directory `/var/www/my_site/files/`.
- **autoindex on;**: Enables directory listing, allowing users to see the files in that directory if no specific file is requested.
- **autoindex_exact_size off;**: Displays human-readable file sizes instead of exact byte counts.
- **autoindex_localtime on;**: Shows file timestamps in the server's local timezone.

### yet another example
To serve the files directly from the root of your server (i.e., accessing them via http://192.168.1.190/), the configuration should be
```nginx
server {
    listen 80;
    server_name 192.168.1.190;

    root /var/www/my_site/files;

    location / {
        try_files $uri $uri/ =404;
    }

    autoindex on;
}
```
