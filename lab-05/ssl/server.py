import socket
import ssl
import threading
import os

# Thông tin server
server_address = ('localhost', 12345)
clients = []

def handle_client(ssl_socket):
    try:
        addr = ssl_socket.getpeername()
        print(f"--- Đã kết nối với: {addr}")
        clients.append(ssl_socket)
        
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Nhận từ {addr}: {message}")
            
            # Gửi cho các client khác
            for client in clients[:]: 
                if client != ssl_socket:
                    try:
                        client.send(data)
                    except:
                        if client in clients: clients.remove(client)
    except Exception as e:
        print(f"Thông báo: Một client đã rời đi hoặc lỗi: {e}")
    finally:
        if ssl_socket in clients:
            clients.remove(ssl_socket)
        ssl_socket.close()

# 1. Tạo SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# 2. Nạp chứng chỉ (Đã sửa đường dẫn theo thư mục certificates của bạn)
try:
    context.load_cert_chain(
        certfile="certificates/server-cert.crt", 
        keyfile="certificates/server-key.key"
    )
except Exception as e:
    print(f"LỖI: Không tìm thấy file chứng chỉ trong thư mục 'certificates'!")
    print(f"Chi tiết: {e}")
    exit()

# 3. Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

print("--- SERVER SSL ĐANG CHẠY TẠI localhost:12345 ---")
print("Đang chờ client kết nối...")

# 4. Vòng lặp chấp nhận kết nối
while True:
    try:
        client_sock, client_addr = server_socket.accept()
        
        # Wrap SSL (Đã sửa lỗi dính chữ Trupython)
        ssl_conn = context.wrap_socket(client_sock, server_side=True)
        
        client_thread = threading.Thread(target=handle_client, args=(ssl_conn,))
        client_thread.daemon = True
        client_thread.start()
    except Exception as e:
        print(f"Lỗi khi thiết lập SSL với client: {e}")