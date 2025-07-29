import socket

print("🔍 Trying to resolve domain...")
try:
    ip = socket.gethostbyname("stream.goldrush.dev")
    print(f"✅ Domain resolved to IP: {ip}")
except Exception as e:
    print(f"❌ DNS resolution failed: {e}")
