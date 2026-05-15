# Issues

## Đang Theo Dõi

- Chưa có bug kỹ thuật trong gameplay vì gameplay chưa được triển khai.
- File `docs/project-main/Neko_Idle_Quest_Y_Tuong_Du_An.docx` có trong cấu trúc mục tiêu nhưng chưa tồn tại trong workspace hiện tại.
- Pygame trên Python 3.12 có thể hiện warning `pkg_resources is deprecated` khi import; hiện chưa ảnh hưởng MVP.
- Đã xử lý lỗi spritesheet Neko: frame 2 và 5 có mảnh nhỏ từ frame kế bên, cần crop vùng đọc trong mỗi cell.
- Source tham khảo `E:\FULLSOURCEAVATAR\` là Java/Maven/server-side, không phù hợp để trộn trực tiếp vào Neko Python/Pygame.
- Đã xử lý lỗi menu preview khiến Neko tự đi liên tục: chuyển sang trạng thái `idle` mặc định và chỉ di chuyển khi giữ `A` hoặc `D`.
- Đã xử lý sai thiết kế dash: cơ chế cũ là giữ `Shift` để chạy nhanh, cơ chế mới là bấm `Shift` một lần để lao một đoạn cố định.

## Ghi Chú Quy Trình

- Hai file quy tắc phát triển ban đầu được tìm thấy trong `rules/rules-main/`.
- Đã bổ sung bản tương ứng vào `docs/project-main/` để AI mới có thể đọc đúng vị trí chuẩn.
