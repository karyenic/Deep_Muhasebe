# -*- coding: utf-8 -*-
def fix_file_indentation(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
                                                                                                                                                                                                               # Girinti
                                                                                                                                                                                                               # seviyelerini
                                                                                                                                                                                                               # dÃƒÆ’Ã†â€™Ãƒâ€š¼zelt
        fixed_lines = []
        for line in lines:
            # Satır baİ¦Ãƒâ€¦¸ındaki boİ¦Ãƒâ€¦¸lukları say
            indent_count = len(line) - len(line.lstrip())
            # 2 boİ¦Ãƒâ€¦¸luk varsa 4 boİ¦Ãƒâ€¦¸luÃƒÆ’Ã¢â‚¬Å¾Ãƒâ€¦¸a ÃƒÆ’Ã†â€™Ãƒâ€š§evir
            if indent_count % 2 == 0:
                new_indent = ' ' * (indent_count * 2)
                fixed_lines.append(new_indent + line.lstrip())
            else:
                fixed_lines.append(line)
                                                                                                                                                                                                               # Dosyayı
                                                                                                                                                                                                               # geri
                                                                                                                                                                                                               # yaz
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
    if __name__ == "__main__":
        # TÃƒÆ’Ã†â€™Ãƒâ€š¼m Python dosyalarını dÃƒÆ’Ã†â€™Ãƒâ€š¼zelt
        for root, dirs, files in os.walk("C:\\YEDEK\OK2_muhasebe"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print(f"DÃƒÆ’Ã†â€™Ãƒâ€š¼zeltiliyor: {file_path}")
                    fix_file_indentation(file_path)
        print("TÃƒÆ’Ã†â€™Ãƒâ€š¼m girintiler dÃƒÆ’Ã†â€™Ãƒâ€š¼zeltildi!")




