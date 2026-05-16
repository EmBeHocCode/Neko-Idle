# Neko Idle Quest: Hành Trình Tri Thức

**Neko Idle Quest: Hành Trình Tri Thức** là game **2D Idle RPG / Auto Battle** được phát triển bằng **Python** và **Pygame**.

Người chơi đồng hành cùng chú mèo Neko trong hành trình vượt ải, chiến đấu tự động với quái vật, nhận vàng, EXP, trang bị, nâng cấp sức mạnh và đánh boss để mở khóa khu vực mới.

## Mục Tiêu Dự Án

Dự án được thực hiện để tham gia cuộc thi **"Thiết kế Game bằng AI"** của trường.

- Xây dựng game 2D hoàn chỉnh bằng Python + Pygame.
- Hoàn thành MVP ổn định trước khi thêm tính năng nâng cao.
- Ứng dụng AI trong tạo tài nguyên, thiết kế gameplay, cân bằng chỉ số và viết tài liệu.
- Có thể đóng gói thành file `.exe` để trình bày trước ban giám khảo.

## Gameplay Chính

- Neko tự động chiến đấu với quái vật.
- Người chơi nhận vàng, EXP và trang bị sau trận.
- Người chơi nâng cấp chỉ số để vượt stage và boss.
- Boss được dùng làm mốc mở khóa khu vực mới.

## Tính Năng Dự Kiến

- Menu chính.
- Auto combat.
- HP, attack, defense, crit.
- Level, EXP, gold.
- Trang bị và kho đồ.
- Boss battles.
- Stage và wave progression.
- Save/load bằng JSON.
- UI cơ bản: HP bar, EXP bar, gold, level, button.

## Công Nghệ Sử Dụng

- Python
- Pygame
- JSON
- Git/GitHub

Nền tảng mục tiêu: **Windows PC**.

## Ứng Dụng AI

AI được sử dụng để hỗ trợ:

- Tạo hình ảnh nhân vật, quái vật, boss, background và icon.
- Thiết kế gameplay, cân bằng chỉ số và progression.
- Viết mô tả kỹ năng, nội dung trình bày và tài liệu dự án.
- Hỗ trợ lập trình, sửa lỗi và tối ưu mã nguồn.

## Cấu Trúc Thư Mục

```text
Neko-Idle/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── res/
│   ├── images/
│   │   ├── characters/
│   │   ├── enemies/
│   │   ├── bosses/
│   │   ├── items/
│   │   ├── ui/
│   │   ├── backgrounds/
│   │   ├── effects/
│   │   ├── maps/
│   │   ├── tilesets/
│   │   └── icons/
│   ├── sounds/
│   │   ├── music/
│   │   └── sfx/
│   └── fonts/
├── data/
│   ├── animations/
│   ├── config/
│   ├── maps/
│   ├── save.json
│   ├── enemies.json
│   ├── items.json
│   ├── skills.json
│   └── stages.json
├── docs/
│   ├── project-main/
│   └── note-prj/
├── rules/
│   └── rules-main/
├── src/
│   ├── core/
│   ├── scenes/
│   ├── entities/
│   ├── systems/
│   ├── ui/
│   └── utils/
├── tools/
└── build/
```

## Cài Đặt Môi Trường

Yêu cầu:

- Python 3.10 trở lên
- Pygame

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

## Cách Chạy Game

Hiện tại dự án mới có khung source tối thiểu. Chạy kiểm tra bằng:

```bash
python main.py
```

Sau khi MVP được triển khai, lệnh này sẽ mở cửa sổ game Pygame.

## Trạng Thái Dự Án Hiện Tại

Dự án đang ở giai đoạn dựng nền tảng:

- Repository GitHub đã được tạo.
- Bộ quy tắc phát triển đã được lưu trong `rules/rules-main/` và `docs/project-main/`.
- Thư mục ghi chú kỹ thuật `docs/note-prj/` đã được chuẩn hóa.
- Cấu trúc source theo module đã được tạo.
- Gameplay chính chưa được triển khai.

## Thông Tin Dự Án

- **Tên game:** Neko Idle Quest: Hành Trình Tri Thức
- **Tên nhóm:** Neko Studio
- **Hình thức:** Làm solo
- **Thể loại:** 2D Idle RPG / Auto Battle
- **Công nghệ chính:** Python + Pygame
- **Nền tảng:** Windows PC
- **Phong cách:** Pixel art, dễ thương, fantasy nhẹ nhàng
- **Đối tượng người chơi:** Từ 11 tuổi trở lên

## Ghi Chú Bản Quyền Và Tài Nguyên

Tài nguyên hình ảnh, âm thanh, font chữ và nội dung trong game sẽ được sử dụng theo một trong các nguồn sau:

- Tự tạo.
- Tạo hoặc hỗ trợ tạo bằng AI.
- Tài nguyên miễn phí có giấy phép sử dụng phù hợp.
- Tài nguyên được chỉnh sửa lại để phù hợp với dự án.

Dự án phục vụ mục đích học tập, nghiên cứu và tham gia cuộc thi thiết kế game.
