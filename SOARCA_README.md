
# SOARCA Installation Guide

This guide provides step-by-step instructions to set up SOARCA and its necessary dependencies on a Linux-based system.

---

## Official Installation Link

The official repository and documentation for SOARCA can be found here: [SOARCA GitHub Repository](https://github.com/COSSAS/SOARCA)

---

## **1. Install Go Programming Language**

### **1.1 Remove Existing Go Installation**
Ensure you remove any previous Go installation to avoid conflicts:
```bash
sudo rm -rf /usr/local/go
```

### **1.2 Download the Go Archive**
Download the correct Go archive for your system from the official Go downloads page:
```bash
wget https://go.dev/dl/go1.23.3.linux-amd64.tar.gz
```

### **1.3 Extract the Archive**
Extract the downloaded file into `/usr/local`:
```bash
sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz
```

### **1.4 Update the PATH Environment Variable**
Add `/usr/local/go/bin` to your PATH. To make this change permanent:
1. Open your profile file (`~/.profile` or `/etc/profile` for a system-wide installation):
   ```bash
   nano ~/.profile
   ```
2. Add the following line at the end of the file:
   ```bash
   export PATH=$PATH:/usr/local/go/bin
   ```
3. Apply the changes immediately by running:
   ```bash
   source ~/.profile
   ```

### **1.5 Verify the Installation**
Check if Go is installed correctly:
```bash
go version
```

---

## **2. Install Required Tools**

### **2.1 Install Go Gin Framework**
Install the Gin framework:
```bash
go get -u github.com/gin-gonic/gin
```

### **2.2 Install Swaggo**
Swaggo is used to generate Swagger documentation:
```bash
go install github.com/swaggo/swag/cmd/swag@latest
```
Ensure `$GOPATH/bin` is in your PATH to make the `swag` command globally accessible:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
source ~/.profile
```
Verify installation:
```bash
swag --version
```

### **2.3 Install Cyclonedx-gomod**
This tool generates CycloneDX SBOMs for Go modules:
```bash
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
```
Ensure it’s in your PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
source ~/.profile
```
Verify installation:
```bash
cyclonedx-gomod version
```

### **2.4 Install Make**
Install the `make` tool:
```bash
sudo apt update
sudo apt install -y build-essential
make --version
```

### **2.5 Install Docker**

#### **a) Install Docker**
```bash
sudo apt update
sudo apt install -y     ca-certificates     curl     gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### **b) Enable Docker for Non-Root Users**
```bash
sudo usermod -aG docker $USER
newgrp docker
```
Verify Docker installation:
```bash
docker --version
docker compose version
```

#### **c) Install Docker Compose (Optional, if not included with Docker)**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<=tag_name": ")[^"]*')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

## **3. Install and Run SOARCA**

### **3.1 Clone the SOARCA Repository**
Clone the repository from GitHub:
```bash
git clone https://github.com/COSSAS/SOARCA.git
cd SOARCA
```

### **3.2 Build the SOARCA Application**
Build SOARCA from source:
```bash
make build
```

### **3.3 Copy Configuration File**
Copy the example configuration file `.env.example` to `.env`:
```bash
cp .env.example .env
```

### **3.4 Run SOARCA**
Start the SOARCA application:
```bash
./build/soarca
```

---

## **4. Running SOARCA via Docker (Alternative)**

### **4.1 Pull the Docker Image**
```bash
docker pull cossas/soarca
```

### **4.2 Run SOARCA with Docker**
Run the SOARCA container:
```bash
docker run -d -p 8080:8080 cossas/soarca
```

---

## **5. Verify SOARCA Setup**

Access the Swagger UI at: [http://localhost:8080/swagger/index.html](http://localhost:8080/swagger/index.html) or interact with SOARCA via the Cacao Roaster or using a command like:

```bash
curl -X POST -H "Content-Type: application/json" --data @playbook.json http://localhost:8080/trigger/playbook
```
(Ensure you are in the playbook directory when running this command.)

Refer to the SOARCA documentation for further details on configuration and usage. **<u>Note that SOARCA is still under development.</u>**
