import psutil
import logging
import asyncio
from telegram import Bot

# Thông tin xác thực
BOT_TOKEN = '8661069362:AAHTMiqT2V6Qp8X6HUadpr0cPNhX8ytFDc8'
CHAT_ID = '8688733295'

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO, 
    filename="system_monitor_bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def log_info(category, message):
    log_msg = f"{category}: {message}"
    logger.info(log_msg)
    print(log_msg)

async def send_telegram_message(bot, message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        log_info("Error", f"Không thể gửi tin nhắn Telegram: {e}")

async def monitor_system():
    # Khởi tạo Bot một lần duy nhất để tối ưu hiệu năng
    bot = Bot(token=BOT_TOKEN)
    log_info("System Monitor", "Bắt đầu giám sát hệ thống (Async Mode)...")

    while True:
        # Lấy thông số hệ thống
        cpu_percent = psutil.cpu_percent(interval=1) # interval giúp đo chính xác hơn
        memory_info = psutil.virtual_memory()

        log_info("CPU", f"Usage: {cpu_percent}%")
        log_info("Memory", f"Usage: {memory_info.percent}%")

        # Chuẩn bị nội dung và gửi tin nhắn bất đồng bộ
        message = f"📊 **Báo cáo hệ thống**\n- CPU: {cpu_percent}%\n- RAM: {memory_info.percent}%"
        
        # Chạy tác vụ gửi tin nhắn mà không làm dừng vòng lặp chính
        await send_telegram_message(bot, message)

        log_info("System Monitor", "------------------------------------------")
        
        # Thay vì time.sleep (làm treo cả chương trình), ta dùng asyncio.sleep
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(monitor_system())
    except KeyboardInterrupt:
        log_info("System Monitor", "Đã dừng chương trình bởi người dùng.")