# Changelog

## 2026-05-16

- Chuyển menu preview của Neko từ tự động đi qua lại sang điều khiển bằng input.
- Trạng thái mặc định của Neko là `idle`; giữ `A` hoặc `D` để di chuyển và phát animation `walk`.
- Thêm animation dash 3 frame cho Neko: `dash_1.png` đến `dash_3.png`; giữ `Shift` khi di chuyển sẽ phát animation `dash`.
- Đổi cơ chế dash từ tăng tốc khi giữ `Shift` sang bấm `Shift` một lần để lao một đoạn cố định, cấu hình bằng `distance` và `duration`.
- Sửa lỗi điều khiển ở rìa màn hình: input `A`/`D` được lưu bằng sự kiện `KEYDOWN`/`KEYUP`, và dash 0px khi đâm vào rìa sẽ không khóa trạng thái nhân vật.

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
