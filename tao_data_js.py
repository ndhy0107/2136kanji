import pandas as pd
from pathlib import Path

# --- Tìm file Excel trong thư mục hiện tại ---
excel_files = list(Path().glob("*.xlsx")) + list(Path().glob("*.xls"))
if not excel_files:
    print("❌ Không tìm thấy file Excel nào!")
    exit()

excel_file = excel_files[0]
print(f"📖 Đang đọc file: {excel_file.name}")

# --- Đọc dữ liệu (3 cột: A, B, C) ---
df = pd.read_excel(excel_file, dtype=str)

# Lấy tên cột (giả sử cột A, B, C)
col_kanji = df.columns[0]      # Cột A: chữ Hán
col_meaning1 = df.columns[1]    # Cột B: nghĩa chính (tiếng Anh hoặc gốc)
col_meaning2 = df.columns[2]    # Cột C: nghĩa tiếng Việt (mới thêm)

print(f"✓ Cột chữ Hán: {col_kanji}")
print(f"✓ Cột nghĩa chính: {col_meaning1}")
print(f"✓ Cột nghĩa tiếng Việt: {col_meaning2}")

# --- Tạo mảng dữ liệu cho JavaScript ---
vocab_items = []
for idx, row in df.iterrows():
    kanji = str(row[col_kanji]).strip() if pd.notna(row[col_kanji]) else ""
    meaning1 = str(row[col_meaning1]).strip() if pd.notna(row[col_meaning1]) else ""
    meaning2 = str(row[col_meaning2]).strip() if pd.notna(row[col_meaning2]) else ""
    
    if kanji:  # Chỉ thêm nếu có chữ Hán
        # Thoát ký tự đặc biệt để tránh lỗi JavaScript
        meaning1_escaped = meaning1.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
        meaning2_escaped = meaning2.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
        
        vocab_items.append(f'  {{ kanji: "{kanji}", meaning: "{meaning1_escaped}", vietnamese: "{meaning2_escaped}" }}')

# --- Ghi ra file data.js ---
with open("data.js", "w", encoding="utf-8") as f:
    f.write("// Dữ liệu từ vựng được tạo tự động từ Excel\n")
    f.write("const vocabulary = [\n")
    f.write(",\n".join(vocab_items))
    f.write("\n];\n")
    f.write(f"\n// Tổng số từ: {len(vocab_items)}\n")

print(f"\n✅ Đã tạo file data.js thành công với {len(vocab_items)} từ vựng!")
print("📁 Hãy copy file data.js này vào thư mục gốc của repository 2136kanji")