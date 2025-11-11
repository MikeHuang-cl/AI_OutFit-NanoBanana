import os
folder_path = "C:\\Users\\mike_huang.CLT\\Desktop\\report\\Style_014_Halloween_Ruins"
target_str = "__4"



def delete_files_with_characters(folder_path, target_str):
    # 瀏覽資料夾中的所有檔案
    for filename in os.listdir(folder_path):
        # 檢查檔名中是否包含指定的字元
        if target_str in filename:
            # 組合出檔案的完整路徑
            file_path = os.path.join(folder_path, filename)
            # 確保這是個檔案而非資料夾
            if os.path.isfile(file_path):
                try:
                    # 刪除檔案
                    os.remove(file_path)
                    print(f"已刪除檔案: {file_path}")
                except Exception as e:
                    print(f"無法刪除檔案 {file_path}: {e}")
            else:
                print(f"{file_path} 不是檔案，跳過.")
        else:
            print(f"{filename} 不包含目標字元，跳過.")


delete_files_with_characters(folder_path, target_str)
