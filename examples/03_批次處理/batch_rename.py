#!/usr/bin/env python3
"""
批次重新命名照片檔案
將檔名改為：旅遊_001.jpg、旅遊_002.jpg 等格式
"""

import os
import sys
from pathlib import Path

def batch_rename_photos(folder_path, prefix="旅遊", dry_run=True):
    """
    批次重新命名照片
    
    Args:
        folder_path: 照片資料夾路徑
        prefix: 檔名前綴
        dry_run: True 只預覽，False 實際執行
    """
    
    folder = Path(folder_path)
    
    # 取得所有jpg檔案，排序
    image_files = sorted(folder.glob("*.jpg"))
    
    if not image_files:
        print(f"❌ 在 {folder_path} 找不到 .jpg 檔案")
        return
    
    print(f"\n📋 找到 {len(image_files)} 個檔案\n")
    print("=" * 70)
    print(f"{'原檔名':<30} → {'新檔名':<30}")
    print("=" * 70)
    
    # 預覽並記錄改名計畫
    rename_plan = []
    for index, old_file in enumerate(image_files, start=1):
        new_name = f"{prefix}_{index:03d}.jpg"
        print(f"{old_file.name:<30} → {new_name:<30}")
        rename_plan.append((old_file, new_name))
    
    print("=" * 70)
    
    if dry_run:
        print("\n✅ 預覽完成（未實際改名）")
        return rename_plan
    else:
        print("\n⚙️  開始執行改名...\n")
        # 執行改名
        for old_file, new_name in rename_plan:
            new_path = old_file.parent / new_name
            try:
                old_file.rename(new_path)
                print(f"✅ {old_file.name} → {new_name}")
            except Exception as e:
                print(f"❌ {old_file.name}: {e}")
        
        print("\n✨ 改名完成！")


if __name__ == "__main__":
    folder_path = "/workspaces/StarPilot/examples/03_批次處理/測試資料/待重新命名"
    
    # 檢查是否有 --execute 參數
    execute_mode = "--execute" in sys.argv
    
    if execute_mode:
        print("🔍 執行模式：\n")
        batch_rename_photos(folder_path, prefix="旅遊", dry_run=False)
    else:
        # 首先預覽
        print("🔍 預覽模式：\n")
        batch_rename_photos(folder_path, prefix="旅遊", dry_run=True)
        
        # 如果確認無誤，取消註解下面這行來執行實際改名
        print("\n" + "!" * 70)
        print("如果預覽結果符合需求，執行以下命令來完成改名：")
        print("!" * 70)
        print("\npython3 /workspaces/StarPilot/examples/03_批次處理/batch_rename.py --execute\n")
