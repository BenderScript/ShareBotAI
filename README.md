# GenAI Sharepoint RAG Chatbot

**Objective**: The primary goal of this demo was to showcase a RAG Chatbot utilizing data from a Sharepoint folder.

**Process Overview**:
1. **Connection to Sharepoint**: The system establishes a connection to a specific Sharepoint folder.
2. **Data Acquisition**: It downloads all the files contained within the folder.
3. **Data Processing**: The files are then processed differently based on their type. For instance, Word documents, PowerPoint presentations, and CSV files each have a unique processing method. The appropriate GenAI chunker & splitter is utilized for each file type.
4. **Video File Handling**: In the case of video files (MP4), the system extracts the audio, breaks it down into manageable parts, and uses OpenAI for transcription.
5. **Data Storage**: All processed information is stored in a VectorDB.
6. **Chatbot Creation**: Utilizing this data, a chatbot is created based on GPT-4 that can answer questions derived from the information in these files.

# How to Run

## .env file

Create a `.env` file with the following information:

```bash
OPENAI_API_KEY=<your open ai key>
OPENAI_API_TEMPERATURE=0.6
OPENAI_API_MODEL_NAME=gpt-4
OFFICE365_CLIENT_ID=<client id>
OFFICE365_CLIENT_SECRET=<client secret>
SHAREPOINT_SITE_URL=https://example.sharepoint.com/sites/myside
SHAREPOINT_FOLDER=Shared Documents/Engineering/genai
```

## Installing Dependencies

```bash
pip3 install -r requirements.txt
```

## Running

Running `bootstrap.py` will open a browser tab with the streamlit interface. 

```bash
python3 bootstrap.py
```

# Areas for Improvement

While the demo was successful, there are opportunities for enhancement. One significant aspect is the preparation of documents before processing. Encouraging users to provide more detailed information about the documents or leveraging GPT-4 to summarize the text could greatly enhance the chatbot's ability to provide insightful responses.

# How to connect to SharePoint Online and SharePoint 2013 2016 2019 on premises with app principal

https://github.com/vgrem/Office365-REST-Python-Client/wiki/How-to-connect-to-SharePoint-Online-and-and-SharePoint-2013-2016-2019-on-premises--with-app-principal

# Using Streamlit with Self-Signed SSL Certificate (Optional)

https://docs.streamlit.io/library/advanced-features/https-support


# Generating a Self-Signed SSL Certificate for Localhost on MacOS

This guide provides steps to generate a self-signed SSL certificate specifically for `https://localhost:8501` on MacOS, using OpenSSL.

## Prerequisites

- Ensure that OpenSSL is installed on your system. If not, you can install it using Homebrew.

## Instructions

### Step 1: Open Terminal

Open the Terminal application, which can be found in the Applications under Utilities, or searched for using Spotlight.

### Step 2: Check for OpenSSL

Check if OpenSSL is installed by typing the following command in Terminal:

```bash
openssl version
```

If it's not installed, install it using Homebrew:

```bash
brew install openssl
```

### Step 3: Create a Private Key

Generate a private key with:

```bash
openssl genrsa -out localhost.key 2048
```

### Step 4: Create a Certificate Signing Request (CSR)

Generate a CSR using the private key:

```bash
openssl req -new -key localhost.key -out localhost.csr
```

When prompted for the "Common Name" (CN), enter `localhost`.

### Step 5: Create a Configuration File

Create a file named `localhost.conf` with the following content:

```
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req

[req_distinguished_name]

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
```

### Step 6: Generate the Self-Signed Certificate

Generate the certificate using your CSR, private key, and the configuration file:

```bash
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -extfile localhost.conf -extensions v3_req -out localhost.crt
```

### Step 7: Verify the Certificate

Check your certificate:

```bash
openssl x509 -text -noout -in localhost.crt
```

### Step 8: Using the Certificate

The `localhost.key` is your private key, and `localhost.crt` is your self-signed certificate. These can be used in your server configuration.

## Note

This self-signed certificate is only suitable for local development and testing. For production environments, consider using a certificate from a trusted Certificate Authority.

