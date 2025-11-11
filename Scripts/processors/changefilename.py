import os

# 設定目標資料夾的路徑
folder_path = 'C:\\Users\\mike_huang.CLT\\Desktop\\Source_Male\\Source1'

# 取得資料夾內的所有檔案
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # 檢查是否是檔案 (避免資料夾)
    if os.path.isfile(file_path):
        # 分割檔案名稱和副檔名
        name, ext = os.path.splitext(filename)
        
        # 新檔案名稱
        new_name = name + '-1' + ext
        
        # 取得新的檔案路徑
        new_file_path = os.path.join(folder_path, new_name)
        
        # 重新命名檔案
        os.rename(file_path, new_file_path)

print("檔名修改完成！")