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
- `src/core/data_manager.py`: nạp và cache JSON game data.
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

- `src/core/sprite_sheet.py` cung cấp hàm cắt spritesheet theo số cột/hàng và hàm đọc danh sách frame rời.
- Animation idle hiện tại của Neko dùng 3 frame rời: `idle_1.png`, `idle_2.png`, `idle_3.png`.
- Frame được trim vùng trong suốt và scale theo chiều cao để dễ đặt vào scene.
- Loader hỗ trợ `cell_crop` để cắt bỏ vùng dư trong từng ô spritesheet khi ảnh AI có mảnh lạc từ frame kế bên.

## Data-Driven Structure

- `data/animations/characters.json`: cấu hình frame rời hoặc spritesheet, tốc độ frame và crop.
- Animation character hỗ trợ cả spritesheet và danh sách frame rời qua `frame_files`.
- `data/maps/forest_path.json`: dữ liệu map mẫu, spawn point, object và NPC.
- `data/config/game_config.json`: cấu hình game tổng quát để mở rộng sau.
- Cấu trúc này tham khảo ý tưởng `GameDataManager` và `res/data/` từ `E:\FULLSOURCEAVATAR\`, nhưng triển khai bằng Python/JSON.

## Ghi Chú Hiện Tại

- Source hiện đã có vòng lặp Pygame tối thiểu.
- Bước tiếp theo là triển khai entity runtime và auto combat cơ bản dựa trên dữ liệu JSON.
