import pandas as pd
from pathlib import Path

current_folder = Path(__file__).parent
excel_files = list(current_folder.glob("*.xlsx")) + list(current_folder.glob("*.xls"))
excel_file = excel_files[0]

df = pd.read_excel(excel_file, dtype=str)
col_name = 'A' if 'A' in df.columns else df.columns[0]
col_meaning = 'B' if 'B' in df.columns else df.columns[1]

# Tạo dữ liệu JavaScript
vocab_list = []
for idx, row in df.iterrows():
    kanji = str(row[col_name]) if not pd.isna(row[col_name]) else ""
    meaning = str(row[col_meaning]) if not pd.isna(row[col_meaning]) else ""
    if kanji:
        vocab_list.append(f'    {{ kanji: "{kanji}", meaning: "{meaning}" }}')

# Ghi file data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Dữ liệu từ vựng tự động tạo từ Excel\n")
    f.write("const vocabulary = [\n")
    f.write(",\n".join(vocab_list))
    f.write("\n];\n")

print(f"✅ Đã tạo file data.js với {len(vocab_list)} từ vựng")