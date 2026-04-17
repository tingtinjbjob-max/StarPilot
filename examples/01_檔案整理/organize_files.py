#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檔案分類工具
按檔案類型將檔案分類到不同的資料夾中
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


def get_file_category(filename):
    """根據檔案副檔名判斷檔案類型"""
    ext = Path(filename).suffix.lower()

    category_map = {
        # 文件類
        '.pdf': '文件',
        '.docx': '文件',
        '.doc': '文件',
        '.xlsx': '文件',
        '.xls': '文件',
        '.txt': '文件',

        # 圖片類
        '.jpg': '圖片',
        '.jpeg': '圖片',
        '.png': '圖片',
        '.gif': '圖片',
        '.bmp': '圖片',

        # 影片類
        '.mp4': '影片',
        '.avi': '影片',
        '.mkv': '影片',
        '.mov': '影片',
    }

    return category_map.get(ext, '其他')


def preview_organization(source_folder):
    """預覽檔案整理方案"""
    files_by_category = defaultdict(list)

    for filename in os.listdir(source_folder):
        filepath = os.path.join(source_folder, filename)

        # 略過資料夾和特殊檔案
        if os.path.isdir(filepath) or filename.startswith('.') or filename == 'README.md':
            continue

        category = get_file_category(filename)
        files_by_category[category].append(filename)

    return files_by_category


def organize_files(source_folder, dry_run=True):
    """
    整理檔案到分類資料夾

    Args:
        source_folder: 來源資料夾路徑
        dry_run: 如果為 True，只顯示預覽；如果為 False，執行真實移動
    """
    files_by_category = preview_organization(source_folder)

    print("=" * 60)
    print("📁 檔案分類預覽")
    print("=" * 60)

    total_files = 0

    for category in sorted(files_by_category.keys()):
        files = files_by_category[category]
        count = len(files)
        total_files += count

        print(f"\n📂 {category}/ ({count} 個檔案)")
        print("-" * 40)
        for filename in sorted(files):
            print(f"   ✓ {filename}")

    print("\n" + "=" * 60)
    print(f"總計: {total_files} 個檔案，分類為 {len(files_by_category)} 種")
    print("=" * 60)

    if dry_run:
        print("\n💡 這是預覽模式。執行 organize_files(..., dry_run=False) 來真正移動檔案。\n")
        return

    # 執行實際移動
    print("\n開始移動檔案...")

    for category in files_by_category.keys():
        category_folder = os.path.join(source_folder, category)

        # 建立分類資料夾
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
            print(f"✅ 建立資料夾: {category}/")

        # 移動檔案
        for filename in files_by_category[category]:
            src = os.path.join(source_folder, filename)
            dst = os.path.join(category_folder, filename)
            shutil.move(src, dst)
            print(f"   ➜ {filename} → {category}/")

    print("\n✨ 檔案整理完成！")


if __name__ == "__main__":
    # 測試資料夾路徑
    test_folder = "/workspaces/StarPilot/examples/01_檔案整理/測試資料_待整理"

    print("\n🚀 START: 檔案整理工具\n")

    # 先預覽
    organize_files(test_folder, dry_run=True)

    # 取得使用者確認
    response = input("✅ 確認無誤後，輸入 'yes' 執行整理: ").strip().lower()

    if response == 'yes':
        organize_files(test_folder, dry_run=False)
    else:
        print("\n❌ 已取消操作。")
