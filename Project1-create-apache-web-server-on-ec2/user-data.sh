#!/bin/bash
# Update system and install Apache
dnf update -y
dnf install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Set permissions for web root
chown -R ec2-user:ec2-user /var/www/html

# Add custom web page
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Welcome to My Custom Apache Server</title>
  <style>
    body {
      background-color: #f0f8ff;
      font-family: 'Segoe UI', sans-serif;
      text-align: center;
      padding: 40px;
    }
    .box {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
      display: inline-block;
    }
    h1 {
      color: #2c3e50;
    }
    p {
      color: #555;
    }
  </style>
</head>
<body>
  <div class="box">
    <h1>Hello from Apache on EC2!</h1>
    <p>This web server is hosted on Amazon Linux 2023.</p>
    <p>Deployed automatically using User Data 🎉</p>
  </div>
</body>
</html>
EOF

# Restart Apache to apply changes
systemctl restart httpd
