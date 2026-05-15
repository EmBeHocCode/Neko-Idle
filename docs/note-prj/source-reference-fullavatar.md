# FULLSOURCEAVATAR Reference Notes

## Nguồn Tham Khảo

- Đường dẫn đã xem: `E:\FULLSOURCEAVATAR\`
- Công nghệ nguồn mẫu: Java 11 + Maven + MySQL + resource `.dat`.
- Ghi chú quan trọng: nguồn mẫu chỉ dùng để tham khảo tổ chức dữ liệu và module, không chuyển Neko Idle Quest khỏi Python/Pygame.

## Cấu Trúc Đáng Học

- `model/`: định nghĩa dữ liệu như map item, NPC, user, position.
- `manager/`: nạp và giữ dữ liệu dùng chung, ví dụ `GameDataManager`.
- `play/`: logic map, zone, object trong màn chơi.
- `service/`: xử lý hành vi/game service.
- `res/data/`: dữ liệu game tách khỏi code.

## Áp Dụng Cho Neko Idle Quest

- Giữ Python + Pygame làm nền tảng chính.
- Dữ liệu animation, map, NPC và object sẽ ưu tiên đặt trong JSON.
- Code Python chỉ đọc dữ liệu và render/chạy logic, hạn chế hard-code vị trí hoặc thông số.
- `DataManager` trong `src/core/data_manager.py` đóng vai trò tương tự lớp nạp dữ liệu trung tâm nhưng đơn giản hơn, phù hợp MVP.

## Quyết Định Kỹ Thuật

- Không copy Java source, `.jar`, `.dat` hoặc database từ FULLSOURCEAVATAR vào Neko.
- Chỉ áp dụng ý tưởng cấu trúc: data-driven, manager/loader, map object/NPC tách khỏi code.
- Các file JSON mới là bước chuẩn bị để sau này chỉnh nhân vật, vật thể và NPC mà không phải sửa nhiều Python.
