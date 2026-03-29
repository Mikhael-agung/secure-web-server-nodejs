import requests
import json
from datetime import datetime
import urllib3

# Disable SSL warnings untuk development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SSLClient:
    def __init__(self, base_url):
        self.base_url = base_url
        
    def test_connection(self):
        """Test koneksi ke server SSL"""
        print("=" * 60)
        print("🔒 Testing SSL/TLS Connection")
        print("=" * 60)
        
        try:
            response = requests.get(self.base_url, verify=False)
            
            print(f"\n✅ Status Code: {response.status_code}")
            print(f"📡 URL: {response.url}")
            print(f"🔐 HTTPS: {'YES ✓' if response.url.startswith('https') else 'NO ✗'}")
            
            data = response.json()
            print(f"\n📦 Response Data:")
            print(json.dumps(data, indent=2))
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
    
    def send_data(self, payload):
        """Kirim data ke server via SSL"""
        print("\n" + "=" * 60)
        print("📤 Sending Data via SSL/TLS")
        print("=" * 60)
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.base_url, 
                json=payload, 
                headers=headers,
                verify=False
            )
            
            print(f"\n✅ Status Code: {response.status_code}")
            
            data = response.json()
            print(f"\n📦 Server Response:")
            print(json.dumps(data, indent=2))
            
            # Tampilkan SSL Info
            if 'ssl_info' in data:
                ssl = data['ssl_info']
                print(f"\n🔐 SSL/TLS Information:")
                print(f"   - Protocol: {ssl.get('ssl_protocol', 'N/A')}")
                print(f"   - Cipher: {ssl.get('ssl_cipher', 'N/A')}")
                print(f"   - Server: {ssl.get('server_name', 'N/A')}")
            
            return data
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None

def main():
    # URL server SSL Node.js
    SERVER_URL = "https://localhost:3443"
    
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "SSL/TLS CLIENT DEMO" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    
    client = SSLClient(SERVER_URL)
    
    # Test 1: Cek koneksi
    if client.test_connection():
        
        # Test 2: Kirim data
        test_data = {
            "nama": "Mikhael Agung",
            "npm": "123456789",
            "mata_kuliah": "Keamanan Jaringan",
            "pesan": "Testing SSL/TLS connection",
            "timestamp": datetime.now().isoformat()
        }
        
        client.send_data(test_data)
        
        print("\n" + "=" * 60)
        print("✅ Demo SSL/TLS Selesai!")
        print("=" * 60)

if __name__ == "__main__":
    main()