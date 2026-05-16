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
res/
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
- `res/`: hình ảnh, âm thanh và font.

## Pygame Loop

- `Game` trong `src/core/game.py` chịu trách nhiệm khởi tạo Pygame, tạo cửa sổ, quản lý clock/FPS và gọi scene hiện tại.
- `MenuScene` là scene đầu tiên, render màn hình khởi động MVP-1.
- `MenuScene` hiện là full-window preview scene: không còn panel/card hoặc text tạm, chỉ vẽ nền toàn màn và Neko.
- `Game.run(max_frames=...)` hỗ trợ test headless để kiểm tra loop mà không cần mở cửa sổ lâu.

## Sprite Sheet

- `src/core/sprite_sheet.py` cung cấp hàm cắt spritesheet theo số cột/hàng và hàm đọc danh sách frame rời.
- Animation idle của Neko dùng sprite sheet `res/images/characters/idle.png`.
- Animation walk của Neko dùng sprite sheet `res/images/characters/walk.png`.
- Animation jump của Neko dùng sprite sheet `res/images/characters/jump.png`.
- Sprite sheet được cắt theo `frame_count`, trim vùng trong suốt, scale theo `render_height`, rồi đặt vào canvas cố định bằng anchor `midbottom` để giữ vị trí ổn định giữa các animation.
- `neko.render_height` trong `data/animations/characters.json` là kích thước render chung cho toàn bộ animation Neko; từng animation vẫn có thể dùng `target_height` riêng nếu cần ngoại lệ.
- Loader hỗ trợ `cell_crop` để cắt bỏ vùng dư trong từng ô spritesheet khi ảnh AI có mảnh lạc từ frame kế bên.
- Loader hỗ trợ `trim_alpha` trong JSON; animation Neko trim phần trong suốt rồi đặt lên canvas cố định để giữ khung render ổn định.
- Loader hỗ trợ `scale_mode: "consistent"` để dùng cùng một tỉ lệ scale cho toàn bộ frame trong một animation; `jump` dùng chế độ này để tránh nhân vật bị to nhỏ giữa các frame.

## Character Input State

- `MenuScene` chọn animation Neko theo trạng thái input thay vì tự chạy preview.
- Không giữ phím di chuyển thì Neko ở trạng thái `idle`.
- Giữ `A` hoặc `D` thì Neko đổi sang `walk`, di chuyển trái/phải và lật mặt theo hướng đi.
- Bấm `Space`, `W` hoặc `Up` thì Neko phát animation `jump`; giai đoạn hiện tại không dùng animation `dash`.
- `jump` tách pose khỏi physics: sprite sheet quyết định pose, còn scene dùng `velocity_y`, `gravity`, `jump_force`, `is_jumping` và `ground_y` để nhân vật bay lên, rơi xuống và tiếp đất.
- Frame `jump` không loop bằng timer; `MenuScene` chọn frame theo tiến trình vật lý của cú nhảy để tránh nhảy từ frame cuối về frame đầu trước khi tiếp đất.
- Với sprite sheet `jump.png` hiện tại, mỗi cell có motion offset lớn từ file vẽ gốc. Vì vậy `pose_mode: "velocity"` chỉ lấy các pose ổn định theo pha bay (`takeoff`, `rise`, `apex`, `fall`, `land`) để đường bay do physics quyết định, không bị double-motion từ ảnh.
- `MenuScene` tự lưu phím đang giữ qua `KEYDOWN`/`KEYUP` để tránh lỗi đọc input không ổn định ở rìa màn hình.
- Nếu `A` và `D` cùng được giữ, phím hướng được bấm gần nhất sẽ được ưu tiên để đổi hướng mượt hơn.
- Biên trái/phải được tính theo nửa chiều rộng frame hiện tại, nên Neko có thể chạm sát mép client nhưng sprite không bị mất khỏi màn; đây là điểm chuẩn để sau này gắn trigger chuyển map.

## Data-Driven Structure

- `data/animations/characters.json`: cấu hình frame rời hoặc spritesheet, tốc độ frame và crop.
- Animation character hiện ưu tiên sprite sheet qua `image` và `frame_count`; danh sách frame rời chỉ còn là fallback kỹ thuật.
- `data/maps/forest_path.json`: dữ liệu map mẫu, spawn point, object và NPC.
- `data/config/game_config.json`: cấu hình game tổng quát để mở rộng sau.
- Cấu trúc này tham khảo ý tưởng `GameDataManager` và `res/data/` từ `E:\FULLSOURCEAVATAR\`, nhưng triển khai bằng Python/JSON.

## Ghi Chú Hiện Tại

- Source hiện đã có vòng lặp Pygame tối thiểu.
- Bước tiếp theo là triển khai entity runtime và auto combat cơ bản dựa trên dữ liệu JSON.
