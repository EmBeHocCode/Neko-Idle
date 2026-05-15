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
- `MenuScene` hiện là full-window preview scene: không còn panel/card hoặc text tạm, chỉ vẽ nền toàn màn và Neko.
- `Game.run(max_frames=...)` hỗ trợ test headless để kiểm tra loop mà không cần mở cửa sổ lâu.

## Sprite Sheet

- `src/core/sprite_sheet.py` cung cấp hàm cắt spritesheet theo số cột/hàng và hàm đọc danh sách frame rời.
- Animation idle của Neko dùng 3 frame rời: `idle_1.png`, `idle_2.png`, `idle_3.png`.
- Animation walk của Neko dùng 5 frame rời: `walk_1.png` đến `walk_5.png`.
- Animation dash của Neko dùng 3 frame rời: `dash_1.png` đến `dash_3.png`.
- Frame được scale theo chiều cao canvas cố định để giữ kích thước ổn định giữa các frame.
- `neko.render_height` trong `data/animations/characters.json` là kích thước render chung cho toàn bộ animation Neko; từng animation vẫn có thể dùng `target_height` riêng nếu cần ngoại lệ.
- Loader hỗ trợ `cell_crop` để cắt bỏ vùng dư trong từng ô spritesheet khi ảnh AI có mảnh lạc từ frame kế bên.
- Loader hỗ trợ `trim_alpha` trong JSON; animation Neko đặt `trim_alpha: false` để giữ khung canvas ổn định và tránh giật kích thước giữa các frame.

## Character Input State

- `MenuScene` chọn animation Neko theo trạng thái input thay vì tự chạy preview.
- Không giữ phím di chuyển thì Neko ở trạng thái `idle`.
- Giữ `A` hoặc `D` thì Neko đổi sang `walk`, di chuyển trái/phải và lật mặt theo hướng đi.
- Bấm `Shift` thì Neko bắt đầu một lượt `dash`, dùng hướng đang giữ bằng `A`/`D`; nếu không giữ hướng thì dash theo hướng đang quay mặt.
- Trong lúc dash, input đi bộ tạm thời không điều khiển vị trí; Neko nội suy từ vị trí bắt đầu đến vị trí đích theo `distance` và `duration` trong `data/animations/characters.json`.
- `MenuScene` tự lưu phím đang giữ qua `KEYDOWN`/`KEYUP` để tránh lỗi đọc input không ổn định ở rìa màn hình.
- Nếu `A` và `D` cùng được giữ, phím hướng được bấm gần nhất sẽ được ưu tiên để đổi hướng mượt hơn.
- Nếu dash bị chặn bởi rìa và vị trí đích trùng vị trí hiện tại, scene bỏ lượt dash đó để không khóa điều khiển.
- Biên trái/phải được tính theo nửa chiều rộng frame hiện tại, nên Neko có thể chạm sát mép client nhưng sprite không bị mất khỏi màn; đây là điểm chuẩn để sau này gắn trigger chuyển map.

## Data-Driven Structure

- `data/animations/characters.json`: cấu hình frame rời hoặc spritesheet, tốc độ frame và crop.
- Animation character hỗ trợ cả spritesheet và danh sách frame rời qua `frame_files`.
- `data/maps/forest_path.json`: dữ liệu map mẫu, spawn point, object và NPC.
- `data/config/game_config.json`: cấu hình game tổng quát để mở rộng sau.
- Cấu trúc này tham khảo ý tưởng `GameDataManager` và `res/data/` từ `E:\FULLSOURCEAVATAR\`, nhưng triển khai bằng Python/JSON.

## Ghi Chú Hiện Tại

- Source hiện đã có vòng lặp Pygame tối thiểu.
- Bước tiếp theo là triển khai entity runtime và auto combat cơ bản dựa trên dữ liệu JSON.
