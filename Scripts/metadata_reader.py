# import os
# import json

# def count_attempts_and_images_generated(directory):
#     count_1_attempt_1_image = 0
#     count_2_attempts_1_image = 0

#     # 遍歷資料夾中的每個檔案
#     for filename in os.listdir(directory):
#         filepath = os.path.join(directory, filename)
        
#         # 只處理檔案（跳過資料夾）
#         if os.path.isfile(filepath):
#             try:
#                 with open(filepath, 'r', encoding='utf-8') as file:
#                     # 嘗試解析 JSON 內容
#                     data = json.load(file)
                    
#                     # 檢查 "attempts" 和 "images_generated" 的條件
#                     if data.get("attempts") == 1 and data.get("images_generated") == 1:
#                         count_1_attempt_1_image += 1
#                     elif data.get("attempts") == 2 and data.get("images_generated") == 1:
#                         count_2_attempts_1_image += 1
#             except Exception as e:
#                 # 如果文件無法解析為 JSON，或者其他錯誤，則跳過
#                 print(f"無法處理檔案 {filename}: {e}")
    
#     return count_1_attempt_1_image, count_2_attempts_1_image

# # 設定要搜尋的資料夾路徑
# directory_path = r'C:\Users\mike_huang.CLT\Desktop\Outfit\test\retry2\Metadata'

# # 呼叫函數並打印結果
# count_1, count_2 = count_attempts_and_images_generated(directory_path)
# print(f"attempts: 1 且 images_generated: 1 的數量: {count_1}")
# print(f"attempts: 2 且 images_generated: 1 的數量: {count_2}")
import os
import json

def count_conditions(directory):
    # 初始化各種條件的計數器
    count_1_attempt_0_image = 0
    count_1_attempt_1_image = 0
    count_1_attempt_no_content_response = 0
    count_1_attempt_blocked_moderation = 0
    count_2_attempt_1_image = 0
    count_2_attempt_0_image = 0
    count_2_attempt_no_content_response = 0
    count_2_attempt_blocked_moderation = 0

    # 遍歷資料夾中的每個檔案
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # 只處理檔案（跳過資料夾）
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    # 嘗試解析 JSON 內容
                    data = json.load(file)
                    
                    # 判斷條件並統計
                    if data.get("attempts") == 1:
                        if data.get("images_generated") == 0:
                            count_1_attempt_0_image += 1
                        elif data.get("images_generated") == 1:
                            count_1_attempt_1_image += 1
                        if "no content parts in response" in data.get("error", ""):
                            count_1_attempt_no_content_response += 1
                        if data.get("content") == "BLOCKED_MODERATION":
                            count_1_attempt_blocked_moderation += 1

                    elif data.get("attempts") == 2:
                        if data.get("images_generated") == 1:
                            count_2_attempt_1_image += 1
                        elif data.get("images_generated") == 0:
                            count_2_attempt_0_image += 1
                        if "no content parts in response" in data.get("error", ""):
                            count_2_attempt_no_content_response += 1
                        if data.get("content") == "BLOCKED_MODERATION":
                            count_2_attempt_blocked_moderation += 1

            except Exception as e:
                # 如果文件無法解析為 JSON，或者其他錯誤，則跳過
                print(f"無法處理檔案 {filename}: {e}")
    
    # 返回所有條件的統計結果
    return {
        "attempts_1_images_0": count_1_attempt_0_image,
        "attempts_1_images_1": count_1_attempt_1_image,
        "attempts_1_no_content_response": count_1_attempt_no_content_response,
        "attempts_1_blocked_moderation": count_1_attempt_blocked_moderation,
        "attempts_2_images_1": count_2_attempt_1_image,
        "attempts_2_images_0": count_2_attempt_0_image,
        "attempts_2_no_content_response": count_2_attempt_no_content_response,
        "attempts_2_blocked_moderation": count_2_attempt_blocked_moderation
    }

# 設定要搜尋的資料夾路徑
directory_path = r'C:\Users\mike_huang.CLT\Desktop\Outfit\test\retry2\Metadata'

# 呼叫函數並打印結果
result = count_conditions(directory_path)

# 顯示統計結果
print(f"attempts: 1 且 images_generated: 0 的數量: {result['attempts_1_images_0']}")
print(f"attempts: 1 且 images_generated: 1 的數量: {result['attempts_1_images_1']}")
print(f"attempts: 1 且 no content parts in response 的數量: {result['attempts_1_no_content_response']}")
print(f"attempts: 1 且 BLOCKED_MODERATION 的數量: {result['attempts_1_blocked_moderation']}")
print(f"attempts: 2 且 images_generated: 1 的數量: {result['attempts_2_images_1']}")
print(f"attempts: 2 且 images_generated: 0 的數量: {result['attempts_2_images_0']}")
print(f"attempts: 2 且 no content parts in response 的數量: {result['attempts_2_no_content_response']}")
print(f"attempts: 2 且 BLOCKED_MODERATION 的數量: {result['attempts_2_blocked_moderation']}")
