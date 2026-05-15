# Architecture Notes

## Định Hướng Kiến Trúc

Dự án hướng tới kiến trúc đơn giản, dễ đọc, dễ mở rộng và phù hợp với game 2D bằng Python + Pygame.

## Nguyên Tắc Chính

- Tách logic game khỏi giao diện hiển thị khi có thể.
- Mỗi module chỉ nên có một trách nhiệm chính.
- Dữ liệu cấu hình nên đặt trong JSON nếu phù hợp.
- Không hard-code dữ liệu cân bằng game nếu dữ liệu đó có khả năng thay đổi thường xuyên.
- Ưu tiên hoàn thành MVP trước khi thêm hệ thống nâng cao.

## Cấu Trúc Dự Kiến

```text
assets/
data/
docs/
docs/note-prj/
src/
tools/
```

## Ghi Chú Hiện Tại

- Chưa có source code game chính thức.
- Kiến trúc chi tiết sẽ được cập nhật khi bắt đầu tạo khung Pygame.

