# Issues

## Đang Theo Dõi

- Chưa có bug kỹ thuật trong gameplay vì gameplay chưa được triển khai.
- File `docs/project-main/Neko_Idle_Quest_Y_Tuong_Du_An.docx` có trong cấu trúc mục tiêu nhưng chưa tồn tại trong workspace hiện tại.
- Pygame trên Python 3.12 có thể hiện warning `pkg_resources is deprecated` khi import; hiện chưa ảnh hưởng MVP.
- Đã xử lý lỗi spritesheet Neko: frame 2 và 5 có mảnh nhỏ từ frame kế bên, cần crop vùng đọc trong mỗi cell.
- Source tham khảo `E:\FULLSOURCEAVATAR\` là Java/Maven/server-side, không phù hợp để trộn trực tiếp vào Neko Python/Pygame.
- Đã xử lý lỗi menu preview khiến Neko tự đi liên tục: chuyển sang trạng thái `idle` mặc định và chỉ di chuyển khi giữ `A` hoặc `D`.
- Animation `dash` đã được loại khỏi giai đoạn hiện tại; hệ thống đang dùng `jump` thay thế.
- Đã xử lý lỗi chạm rìa khiến điều khiển bị kẹt: input di chuyển không phụ thuộc trực tiếp vào `pygame.key.get_pressed()`, và phím hướng mới nhất được ưu tiên khi `A`/`D` cùng được giữ.
- Đã xử lý lỗi animation Neko bị lệch to nhỏ dù sprite sheet khác kích thước: frame sau khi cắt được trim, scale theo `render_height`, rồi đặt vào canvas cố định.
- Đã xử lý cảm giác `jump` bị giật/đơ: nguyên nhân là frame jump bị loop gần lúc tiếp đất và từng frame bị scale riêng theo chiều cao riêng; hiện jump sync theo physics và dùng scale đồng nhất cho cả animation.
- Đã giảm tiếp cảm giác `jump` khựng: sprite sheet `jump.png` có motion offset lớn trong từng cell, nên hệ thống hiện chọn các pose ổn định theo vận tốc thay vì phát toàn bộ frame tuần tự.
- Đã refactor lỗi lệch vị trí/sai frame khi đổi `idle`/`walk`/`jump`: thay loader rải rác trong `MenuScene` bằng `PlayerAnimationSystem`, cache toàn bộ frame một lần, đặt mọi frame player lên canvas 256x256 và vẽ bằng `image.get_rect(midbottom=(self.x, self.y))`.
- Đã chuẩn hóa lại `jump.png` của Neko thành 6 frame ngang đúng với `frame_count = 6`, tránh cắt sai frame do sheet cũ có 12 frame nhưng config mới yêu cầu 6 frame.
- Đã xử lý UI preview còn giống card/menu tạm: bỏ panel viền vàng và text, dùng full-window canvas để chuẩn bị dựng map.
- Đã thêm map layer đầu tiên để thay nền màu phẳng: background và land được vẽ từ `forest_path.json`, land top dùng làm `ground_y` cho va chạm cơ bản.
- Đã xử lý padding đáy của asset `hero_01`: animation được trim rồi đặt lại vào canvas cố định bằng `midbottom`, tránh nhân vật bị nổi trên mặt đất.
- Đã xử lý giới hạn di chuyển còn cách mép quá xa: bỏ biên cố định 80px và clamp theo kích thước frame để Neko sát mép nhưng không biến mất.
- Đã xử lý nguy cơ lệch vị trí khi đổi sprite sheet kích thước khác nhau bằng canvas cố định và anchor `midbottom`.
- Đã xử lý lỗi bấm `Space` chỉ đổi frame jump tại chỗ: thay bằng physics thật với `velocity_y`, `gravity`, `jump_force`, `is_jumping` và `ground_y`; nhân vật tiếp đất về đúng baseline.

## Ghi Chú Quy Trình

- Đã thêm `neko.render_height` để tránh phải sửa lặp lại kích thước trong từng animation.
- Hai file quy tắc phát triển ban đầu được tìm thấy trong `rules/rules-main/`.
- Đã bổ sung bản tương ứng vào `docs/project-main/` để AI mới có thể đọc đúng vị trí chuẩn.
