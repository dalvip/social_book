import certifi
import os

cert_path = certifi.where()
print(f"Certificate path: {cert_path}")

# Set this as an environment variable
os.environ['SSL_CERT_FILE'] = cert_path
os.environ['REQUESTS_CA_BUNDLE'] = cert_path