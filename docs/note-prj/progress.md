# Progress

## Trạng Thái Hiện Tại

- Nhân vật đang được ưu tiên hoàn thiện là `hero_01`; Neko tạm giữ lại trong dữ liệu và chỉ chỉnh khi có yêu cầu riêng.
- `forest_path` hiện dùng `hero_01` làm `player_character` và `preview_characters` mặc định.
- Animation của `hero_01` dùng `scale_mode: "consistent"` với hệ số scale chung toàn bộ animation để tránh lệch kích thước khi đổi trạng thái.
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
- Hệ thống player animation đã được refactor sang `PlayerAnimationSystem`: toàn bộ frame được cắt và cache vào RAM một lần khi scene khởi động.
- Idle/walk/jump của Neko hiện dùng config rõ ràng: `idle` 4 frame, `walk` 8 frame, `jump` 6 frame.
- Mọi frame player được đặt lên canvas cố định 256x256, nền trong suốt, căn baseline bằng `midbottom` để đổi animation không lệch chân.
- Jump physics tách riêng khỏi animation bằng `velocity_y`, `gravity`, `jump_force`, `is_jumping` và `ground_y`; khi tiếp đất sẽ quay lại `idle` hoặc `walk`.
- `Player` data model đã có các field physics cơ bản: `velocity_y`, `gravity`, `jump_force`, `is_jumping`, `ground_y`.
- Kích thước render của idle/walk/jump đã được chuẩn hóa bằng canvas cố định để giảm lệch hình giữa các animation.
- Tốc độ đi bộ thử nghiệm của Neko hiện là 400 px/s.
- Kích thước tổng thể của Neko hiện chỉnh bằng `neko.render_height` trong `data/animations/characters.json`.
- Menu preview hiện dùng toàn bộ cửa sổ game, không còn panel viền vàng hoặc chữ tạm.
- Neko hiện có thể đi tới sát hai mép client nhưng vẫn được giữ trong màn để quay lại.
- Đã có `DataManager` để nạp JSON trung tâm.
- Map preview đầu tiên đã có nền `forest_background.png` và land `forest_land.png` trong `res/images/maps/`.
- `MenuScene` hiện đọc `data/maps/forest_path.json` để vẽ background/land và lấy `ground_y` từ top land làm baseline va chạm cho Neko.
- Đã thêm nhân vật thử nghiệm `hero_01` với full animation từ bộ asset mua ngoài; hiện `hero_01` là nhân vật preview/player mặc định.
- Asset `hero_01` hiện nằm trong `res/images/characters/hero_01/`, gồm sprite sheet theo từng animation và file `preview.png` để xem nhanh.
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
