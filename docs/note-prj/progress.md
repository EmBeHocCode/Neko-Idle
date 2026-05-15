# Progress

## Trạng Thái Hiện Tại

- Dự án đang ở giai đoạn chuẩn bị trước MVP.
- Repository Git đã được khởi tạo và liên kết với GitHub.
- README cơ bản đã được tạo.
- Script hỗ trợ đồng bộ Git đã được thêm.
- Bộ quy tắc phát triển đã có trong `docs/project-main/`.
- Cấu trúc thư mục chính đã được dựng.
- Khung source tối thiểu đã chạy được bằng `python main.py`.
- MVP-1 đã có cửa sổ Pygame, game loop và menu scene đầu tiên.
- Ảnh spritesheet cũ `assets/images/characters/neko-idle.png` đã được thay bằng frame rời.
- Animation idle của Neko đã đọc cấu hình từ `data/animations/characters.json`.
- Animation idle hiện dùng 3 frame rời trong `assets/images/characters/`.
- Animation walk hiện dùng 5 frame rời trong `assets/images/characters/` và đã chạy thử trên menu.
- Đã có `DataManager` để nạp JSON trung tâm.
- Gameplay chính chưa được triển khai.

## Việc Cần Ưu Tiên Tiếp Theo

- Tạo dữ liệu entity runtime cho Neko và slime.
- Ưu tiên MVP tiếp theo: nhân vật, quái, auto combat cơ bản.
- Dùng JSON map/object/NPC khi cần đặt vị trí trong battle scene.
- Sau mỗi tính năng hoàn thành, cập nhật changelog, progress, architecture hoặc issues tương ứng.

## Quy Tắc Đang Áp Dụng

- Luôn đọc và tuân thủ bộ quy tắc phát triển trước khi thay đổi dự án.
- Mọi thay đổi quan trọng phải được ghi vào `docs/note-prj/` bằng Markdown.
- Mỗi tính năng phải được kiểm thử sau khi hoàn thành.
- Commit Git ngắn gọn, rõ ràng và thường xuyên.
