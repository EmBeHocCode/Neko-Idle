# Architecture Notes

## Định Hướng Kiến Trúc

Dự án hướng tới kiến trúc đơn giản, dễ đọc, dễ mở rộng và phù hợp với game 2D bằng Python + Pygame.

## Nguyên Tắc Chính

- Tách logic game khỏi giao diện hiển thị khi có thể.
- Mỗi module chỉ nên có một trách nhiệm chính.
- Dữ liệu cấu hình nên đặt trong JSON nếu phù hợp.
- Không hard-code dữ liệu cân bằng game nếu dữ liệu đó có khả năng thay đổi thường xuyên.
- Ưu tiên hoàn thành MVP trước khi thêm hệ thống nâng cao.

## Cấu Trúc Hiện Tại

```text
assets/
data/
docs/
docs/note-prj/
src/
src/core/
src/scenes/
src/entities/
src/systems/
src/ui/
src/utils/
tools/
build/
```

## Trách Nhiệm Module

- `main.py`: entry point của dự án.
- `src/core/`: điều phối game, settings, asset loader, save manager.
- `src/scenes/`: các màn hình như menu và battle.
- `src/entities/`: dữ liệu nhân vật, quái và boss.
- `src/systems/`: combat, progression, inventory và equipment.
- `src/ui/`: các thành phần giao diện như HP bar, EXP bar, button.
- `src/utils/`: helper và logger dùng chung.
- `data/`: dữ liệu JSON có thể chỉnh để cân bằng game.
- `assets/`: hình ảnh, âm thanh và font.

## Pygame Loop

- `Game` trong `src/core/game.py` chịu trách nhiệm khởi tạo Pygame, tạo cửa sổ, quản lý clock/FPS và gọi scene hiện tại.
- `MenuScene` là scene đầu tiên, render màn hình khởi động MVP-1.
- `Game.run(max_frames=...)` hỗ trợ test headless để kiểm tra loop mà không cần mở cửa sổ lâu.

## Sprite Sheet

- `src/core/sprite_sheet.py` cung cấp hàm cắt spritesheet theo số cột và hàng.
- Ảnh Neko hiện dùng layout 3 cột x 2 hàng, tổng 6 frame.
- Frame được trim vùng trong suốt và scale theo chiều cao để dễ đặt vào scene.

## Ghi Chú Hiện Tại

- Source hiện đã có vòng lặp Pygame tối thiểu.
- Bước tiếp theo là triển khai entity runtime và auto combat cơ bản.
