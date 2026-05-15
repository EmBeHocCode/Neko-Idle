# 🐾 Neko Idle Quest: Hành Trình Tri Thức

**Neko Idle Quest: Hành Trình Tri Thức** là một game **2D Idle RPG / Auto Battle** được phát triển bằng **Python** và **Pygame**.

Người chơi đồng hành cùng chú mèo Neko trong hành trình vượt ải, chiến đấu với quái vật, nhận vàng, EXP, trang bị, nâng cấp sức mạnh và đánh boss để mở khóa khu vực mới.

## 🎯 Mục Tiêu Dự Án

Dự án được thực hiện để tham gia cuộc thi **"Thiết kế Game bằng AI"** của trường.

Mục tiêu chính:

- Xây dựng một game 2D hoàn chỉnh bằng Python + Pygame.
- Tạo gameplay idle/auto battle dễ hiểu, phù hợp với người chơi từ 11 tuổi trở lên.
- Ứng dụng AI trong quá trình tạo tài nguyên, thiết kế gameplay và viết tài liệu.
- Có thể đóng gói thành file `.exe` để trình bày trước ban giám khảo.

## 🌟 Giới Thiệu Ngắn

Trong game, người chơi sẽ điều khiển Neko, một chú mèo chiến binh dễ thương, cầm vũ khí và tự động chiến đấu với quái vật theo từng màn chơi.

Game không thuộc thể loại giải đố. Trọng tâm gameplay là **idle/auto battle**, cày tài nguyên, nâng cấp nhân vật và vượt boss.

## 🎮 Gameplay Chính

- Neko tự động chiến đấu với quái vật.
- Nhận vàng, EXP và trang bị sau khi chiến thắng.
- Nâng cấp chỉ số nhân vật để mạnh hơn.
- Vượt qua các wave và stage.
- Đánh boss để mở khóa khu vực mới.

## ✨ Tính Năng Dự Kiến

- Menu chính.
- Nhân vật Neko và hệ thống quái vật.
- Hệ thống auto combat.
- Chỉ số HP, attack, defense, crit.
- Hệ thống level, EXP và gold.
- Trang bị và kho đồ.
- Boss battles.
- Stage và wave progression.
- Save/load dữ liệu bằng JSON.
- Giao diện người dùng: HP bar, EXP bar, gold, level.

## 🛠 Công Nghệ Sử Dụng

- **Python**
- **Pygame**
- **JSON** cho hệ thống lưu dữ liệu
- Công cụ AI hỗ trợ tạo tài nguyên và nội dung

Nền tảng mục tiêu: **Windows PC**

## 🤖 Ứng Dụng AI

AI được sử dụng để hỗ trợ:

- Tạo hình ảnh nhân vật, quái vật, boss, background và icon.
- Thiết kế gameplay, cân bằng chỉ số và progression.
- Viết mô tả kỹ năng, nội dung trình bày và tài liệu dự án.
- Hỗ trợ lập trình, sửa lỗi và tối ưu mã nguồn.

## 📁 Cấu Trúc Thư Mục Dự Kiến

```text
Neko-Idle/
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── data/
│   ├── save.json
│   └── config.json
├── docs/
├── src/
│   ├── main.py
│   ├── game.py
│   ├── player.py
│   ├── enemy.py
│   ├── combat.py
│   ├── ui.py
│   └── save_load.py
├── README.md
└── requirements.txt
```

## ⚙️ Cài Đặt Môi Trường

Yêu cầu:

- Python 3.10 trở lên
- Pygame

Cài đặt thư viện:

```bash
pip install pygame
```

Hoặc sau này, nếu có file `requirements.txt`:

```bash
pip install -r requirements.txt
```

## ▶️ Cách Chạy Game Sau Này

Sau khi mã nguồn được hoàn thiện, chạy game bằng lệnh:

```bash
python src/main.py
```

## 🚧 Trạng Thái Dự Án Hiện Tại

Dự án đang ở giai đoạn chuẩn bị:

- Lên ý tưởng gameplay.
- Xác định công nghệ sử dụng.
- Thiết kế phạm vi tính năng.
- Chuẩn bị repository.
- Chưa triển khai source code game chính thức.

## 📌 Thông Tin Dự Án

- **Tên game:** Neko Idle Quest: Hành Trình Tri Thức
- **Tên nhóm:** Neko Studio
- **Hình thức:** Làm solo
- **Thể loại:** 2D Idle RPG / Auto Battle
- **Công nghệ chính:** Python + Pygame
- **Nền tảng:** Windows PC
- **Phong cách:** Pixel art, dễ thương, fantasy nhẹ nhàng
- **Đối tượng người chơi:** Từ 11 tuổi trở lên

## 📜 Ghi Chú Bản Quyền Và Tài Nguyên

Tài nguyên hình ảnh, âm thanh, font chữ và nội dung trong game sẽ được sử dụng theo một trong các nguồn sau:

- Tự tạo.
- Tạo hoặc hỗ trợ tạo bằng AI.
- Tài nguyên miễn phí có giấy phép sử dụng phù hợp.
- Tài nguyên được chỉnh sửa lại để phù hợp với dự án.

Dự án phục vụ mục đích học tập, nghiên cứu và tham gia cuộc thi thiết kế game.
