import socket
import ssl
import os

try:
    server_address = ('localhost', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("--- ĐANG KIỂM TRA CHỨNG CHỈ ---")
    # Thay tên file đúng với file bạn thấy trong thư mục VS Code bên trái
    cert_file = "server-cert.crt" 
    key_file = "server-key.key"

    if not os.path.exists(cert_file):
        print(f"LỖI: Không tìm thấy file {cert_file} ở thư mục hiện tại!")
    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        print("--- SERVER ĐANG CHỜ KẾT NỐI (SSL OK) ---")
        
        while True:
            client, addr = server_socket.accept()
            print(f"Có kết nối từ: {addr}")
            
except Exception as e:
    print(f"\n[PHÁT HIỆN LỖI THỰC SỰ]: {e}")
    input("Nhấn Enter để đóng...") # Giữ cửa sổ lại để bạn đọc lỗi