# Changelog

## 2026-05-17

- Thêm nền map đầu tiên cho `forest_path`: `forest_background.png` 1920x1080 và `forest_land.png` 1920x1080 trong `res/images/maps/`.
- Ghép `forest_land.png` từ các tile đất `1.png`, `2.png`, `3.png`, `4.png`; land nằm ở đáy ảnh và dùng `ground_y` trong JSON để làm baseline va chạm.
- Cập nhật `MenuScene` để vẽ background + land từ `data/maps/forest_path.json` trước khi vẽ Neko.
- Làm mượt animation `jump`: frame jump không còn loop bằng timer trong lúc đang bay, mà được chọn theo tiến trình vật lý của cú nhảy.
- Thêm `scale_mode: "consistent"` cho sprite sheet để giữ cùng một tỉ lệ scale trong toàn bộ animation, tránh frame jump bị phóng to/thu nhỏ gây cảm giác giật.
- Đổi `jump` sang `pose_mode: "velocity"`: sprite chỉ đổi các pose ổn định theo pha bay (`takeoff`, `rise`, `apex`, `fall`, `land`) thay vì chạy toàn bộ 12 frame có motion offset sẵn trong ảnh.

## 2026-05-16

- Chuyển hệ thống asset nhân vật từ `assets/` sang `res/`.
- Cập nhật animation Neko từ frame PNG rời sang sprite sheet theo từng animation: `idle.png`, `walk.png`, `jump.png`.
- Bỏ animation `dash` trong giai đoạn hiện tại và thay bằng `jump`; phím nhảy dùng `Space`, `W` hoặc `Up`.
- Sprite sheet được cắt theo `frame_count` trong `data/animations/characters.json`, sau đó trim và đặt vào canvas cố định để không lệch vị trí khi đổi animation.
- Sửa jump sang physics thật: `jump` animation chỉ điều khiển pose/frame, còn vị trí Y dùng `velocity_y`, `gravity`, `jump_force`, `is_jumping` và `ground_y`.
- Bổ sung các field physics cơ bản vào `Player` data model để chuẩn bị tách runtime player khỏi preview scene.
- Chuyển menu preview của Neko từ tự động đi qua lại sang điều khiển bằng input.
- Trạng thái mặc định của Neko là `idle`; giữ `A` hoặc `D` để di chuyển và phát animation `walk`.
- Thêm animation dash 3 frame cho Neko: `dash_1.png` đến `dash_3.png`; giữ `Shift` khi di chuyển sẽ phát animation `dash`.
- Đổi cơ chế dash từ tăng tốc khi giữ `Shift` sang bấm `Shift` một lần để lao một đoạn cố định, cấu hình bằng `distance` và `duration`.
- Sửa lỗi điều khiển ở rìa màn hình: input `A`/`D` được lưu bằng sự kiện `KEYDOWN`/`KEYUP`, và dash 0px khi đâm vào rìa sẽ không khóa trạng thái nhân vật.
- Chuẩn hóa kích thước animation Neko: idle, walk và jump đều render qua canvas cố định để tránh lệch to nhỏ giữa các frame.
- Tăng tốc độ đi bộ của Neko từ 90 lên 150 px/s để cảm giác điều khiển nhanh hơn.
- Thêm `render_height` chung cho Neko trong `data/animations/characters.json`; chỉ cần sửa một giá trị để đổi kích thước toàn bộ idle/walk/jump.
- Ghi nhận cấu hình thử nghiệm hiện tại: `walk.move_speed` của Neko là 400 px/s.
- Chuyển menu preview sang bố cục full-window: bỏ panel viền vàng và toàn bộ text tạm, chỉ giữ nền và Neko để chuẩn bị thay bằng map/gameplay scene.
- Mở rộng giới hạn di chuyển tới sát mép client: Neko được clamp theo nửa frame hiện tại thay vì khoảng cách cố định 80px.

## 2026-05-15

- Khởi tạo tài liệu dự án cơ bản cho repository GitHub.
- Thêm script đồng bộ Git tại `tools/git_sync.ps1`.
- Ghi nhận bộ quy tắc phát triển bắt buộc của dự án.
- Chuẩn hóa thư mục ghi chú kỹ thuật `docs/note-prj/`.
- Bổ sung bản quy tắc phát triển vào `docs/project-main/` theo vị trí chuẩn của dự án.
- Dựng cấu trúc thư mục chính cho dự án: `assets/`, `data/`, `src/`, `docs/`, `rules/`, `tools/`, `build/`.
- Thêm khung source tối thiểu cho các nhóm module `core`, `scenes`, `entities`, `systems`, `ui`, `utils`.
- Thêm dữ liệu JSON mẫu ban đầu cho save, enemy, item, skill và stage.
- Cập nhật README theo cấu trúc dự án mới.
- Triển khai MVP-1: cửa sổ Pygame, game loop cơ bản và menu scene đầu tiên.
- Thêm loader spritesheet và hiển thị animation idle của Neko trên menu.
- Sửa lỗi animation Neko bị lộ mảnh frame kế bên bằng crop nội bộ khi cắt spritesheet.
- Tham khảo cấu trúc `E:\FULLSOURCEAVATAR\` và bổ sung hướng data-driven cho Neko bằng `DataManager`, JSON animation và JSON map.
- Chuyển animation idle của Neko sang 3 frame PNG rời: `idle_1.png` đến `idle_3.png`.
- Thêm animation walk 5 frame cho Neko: `walk_1.png` đến `walk_5.png`, menu preview cho Neko đi qua lại.
