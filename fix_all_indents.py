# -*- coding: utf-8 -*-
import re
    def fix_indentation(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                    # TÃƒÆ’Ã†â€™Ãƒâ€š¼m girintileri 4 boİ¦Ãƒâ€¦¸luk yap
                fixed_content = re.sub(r'^\s+',
    lambda m: ' ' * (len(m.group(0)) * 4),
    content,
     flags=re.MULTILINE)
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(fixed_content)
    if __name__ == "__main__":
                project_dir = r"C:\YEDEK\OK2_muhasebe"
                for root, dirs, files in os.walk(project_dir):
                                for file in files:
                                                if file.endswith(".py"):
                                                                file_path = os.path.join(root, file)
                                                                print(f"Fixing indentation in: {file_path}")
                                                                fix_indentation(file_path)
                print("TÃƒÆ’Ã†â€™Ãƒâ€š¼m Python dosyalarının girintileri dÃƒÆ’Ã†â€™Ãƒâ€š¼zeltildi!")




