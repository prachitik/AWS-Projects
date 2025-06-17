# 🛠️ Troubleshooting & Key Learnings

This document outlines the challenges I encountered while deploying an Apache web server on Amazon EC2, how I resolved them, and what I learned in the process.

---

## ❌ Issue 1: Website Not Loading — "This site can’t be reached"

🔍 **Symptom:**  
- EC2 instance status: ✅ *Running*  
- Tried visiting `http://<public-ip>` → ❌ *This site can’t be reached*

💡 **Diagnosis:**  
- Apache was not properly installed or started  
- EC2 User Data script might not have executed on launch

✅ **Fix:**  
- Needed to SSH into instance to verify setup (but SSH wasn't working initially — see next issue)  
- After regaining SSH access, manually ran Apache install and start commands  
- Alternatively, relaunched EC2 with corrected User Data script

---

## ❌ Issue 2: SSH Access Failed — "Failed to connect to your instance"

🔍 **Symptom:**  
- Error connecting via SSH: *Timeout / Connection failed*

💡 **Diagnosis:**  
- Key pair was not downloaded during instance setup  
- Inbound security rule for port `22` (SSH) was incorrect or missing

✅ **Fix:**  
1. Created a new key pair `aws-custom-apache-webserver-key`  
2. Downloaded `.pem` file and moved it to `~/.ssh/`:
   ```bash
   mv ~/Downloads/aws-custom-apache-webserver-key.pem ~/.ssh/
   chmod 400 ~/.ssh/aws-custom-apache-webserver-key.pem


✅ Final Re-deployment
📋 Relaunched EC2 with the following setup:

Amazon Linux 2023 AMI

User Data to install Apache and deploy a custom HTML page

Security Group with proper inbound rules

Verified success by visiting: http://<EC2-Public-IP>


💡 Key Learnings
💡 Lesson	🔍 Insight
🔐 Secure SSH Access	Always download and properly secure the .pem key
🌍 Security Groups Matter	Ensure correct port permissions: 22 (SSH), 80 (HTTP)
⚙️ User Data Scripting	Validate shell scripts carefully for automation to succeed
🧪 Manual Debugging	SSH access is critical to test and fix issues directly
🛠️ Linux File Permissions	Apache requires correct ownership (chown) and permissions (chmod)
🔁 Clean Setup Helps	Sometimes it's easier to relaunch the instance with clean configuration

🎯 Outcome
🎉 Successfully completed the challenge to:

🚀 Launch an EC2 instance with Amazon Linux 2023

🌐 Install and run Apache web server using User Data

🎨 Host a custom-designed webpage

🔐 Configure SSH and HTTP access via Security Group rules

🧩 Troubleshoot real-world deployment issues

🧠 This project helped reinforce my understanding of:

AWS EC2 instance lifecycle

Linux-based web server deployment

Infrastructure debugging & automation
