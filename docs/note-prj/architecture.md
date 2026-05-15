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

## Ghi Chú Hiện Tại

- Source hiện mới là skeleton, chưa có vòng lặp Pygame thật.
- `main.py` chạy được để kiểm tra nền tảng import và entry point.
- Bước tiếp theo là triển khai cửa sổ Pygame và scene đầu tiên.
