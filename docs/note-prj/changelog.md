# Changelog

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
