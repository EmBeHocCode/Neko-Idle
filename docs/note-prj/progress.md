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
- Thư mục tài nguyên chính hiện chuyển từ `assets/` sang `res/`.
- Animation idle của Neko đã đọc cấu hình từ `data/animations/characters.json`.
- Animation idle/walk/jump hiện dùng sprite sheet riêng trong `res/images/characters/`.
- Menu preview hiện đã có trạng thái `idle`, di chuyển bằng `A`/`D`, và bấm `Space`/`W`/`Up` để phát animation `jump` kèm physics nhảy thật.
- Jump physics hiện dùng `velocity_y`, `gravity`, `jump_force`, `is_jumping` và `ground_y`; khi tiếp đất sẽ quay lại `idle` hoặc `walk`.
- Animation `jump` hiện phát theo tiến trình vật lý của cú nhảy và không loop frame trong lúc đang bay.
- Sprite sheet `jump` hiện dùng `scale_mode: "consistent"` để giữ tỉ lệ scale đồng nhất giữa các frame, giảm cảm giác giật do frame bị to nhỏ bất thường.
- `jump` hiện dùng `pose_mode: "velocity"` để chọn pose theo vận tốc/độ cao, hạn chế khựng do sprite sheet có motion offset sẵn trong từng frame.
- `Player` data model đã có các field physics cơ bản: `velocity_y`, `gravity`, `jump_force`, `is_jumping`, `ground_y`.
- Kích thước render của idle/walk/jump đã được chuẩn hóa bằng canvas cố định để giảm lệch hình giữa các animation.
- Tốc độ đi bộ thử nghiệm của Neko hiện là 400 px/s.
- Kích thước tổng thể của Neko hiện chỉnh bằng `neko.render_height` trong `data/animations/characters.json`.
- Menu preview hiện dùng toàn bộ cửa sổ game, không còn panel viền vàng hoặc chữ tạm.
- Neko hiện có thể đi tới sát hai mép client nhưng vẫn được giữ trong màn để quay lại.
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
