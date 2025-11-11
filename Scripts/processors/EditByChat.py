#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EditByChat.py
自動將資料夾內圖片逐張送進 API (例如 /run_inference)，
解析輸出結果中的功能建議，依分類統計。

輸出：
  1. results_per_image.csv
  2. summary_by_label_feature.csv
"""

import argparse, re, time, sys, json
from pathlib import Path
from typing import List, Tuple
import pandas as pd
from tqdm import tqdm
from gradio_client import Client, handle_file

# 支援的圖片副檔名
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp" , ".jfif."}

def list_images_with_labels(root: Path) -> List[Tuple[Path, str]]:
    """掃描資料夾，推斷每張圖的分類 label。"""
    pairs = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            try:
                rel = p.relative_to(root)
                label = rel.parts[0] if len(rel.parts) >= 2 else "unlabeled"
            except Exception:
                label = "unlabeled"
            pairs.append((p, label))
    pairs.sort(key=lambda x: str(x[0]).lower())
    return pairs

def parse_features_from_result(result) -> List[str]:
    """解析 API 回傳的右側功能清單（如 cool_ct_and_luts）。"""
    if result is None:
        return []

    # 若已是 list[str]
    if isinstance(result, list):
        return [str(x).strip() for x in result if str(x).strip()]

    s = str(result).strip()

    # 嘗試 JSON 格式
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()]
        if isinstance(parsed, dict):
            return [k for k, v in parsed.items() if v]
    except Exception:
        pass

    # 一般文字行
    lines = [x.strip() for x in s.splitlines() if x.strip()]
    cleaned = []
    for ln in lines:
        ln = re.sub(r"^(\s*[-*•]\s*)", "", ln)
        ln = re.sub(r"^\s*\d+\.\s*", "", ln)
        if re.search(r"(功能|feature|apply|將套用)", ln, re.IGNORECASE):
            if ":" in ln:
                tail = ln.split(":", 1)[1].strip()
                if tail:
                    cleaned.append(tail)
            continue
        cleaned.append(ln)

    # 分割符號（中英逗號、頓號）
    feats = []
    for ln in cleaned:
        ln = re.sub(r"\(.*?\)", "", ln)
        for part in re.split(r"[、，,;]+", ln):
            part = part.strip()
            if len(part) > 1:
                feats.append(part)

    uniq = []
    seen = set()
    for f in feats:
        if f not in seen:
            uniq.append(f)
            seen.add(f)
    return uniq

def main():
    ap = argparse.ArgumentParser(description="批次呼叫 API 並彙整圖片輸出結果")
    ap.add_argument("--root", default= "c:\\src", required=True, help="圖片根目錄（含子資料夾作分類）")
    ap.add_argument("--api-url", default="http://210.244.31.10:7006/", help="Gradio 服務 URL")
    ap.add_argument("--api-name", default="/run_inference", help="端點名稱")
    ap.add_argument("--api-key", required=True, default="AIzaSyDwEBqc7QqF0xRSv4LeAg-_QjjKBvCf6qk", help="Gemini API Key")
    ap.add_argument("--model", default="gemini-2.0-flash", help="模型名稱")
    ap.add_argument("--sleep", type=float, default=0.3, help="每張間隔秒數，避免過快")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    pairs = list_images_with_labels(root)
    if not pairs:
        print("❌ 找不到任何圖片。")
        sys.exit(0)

    client = Client(args.api_url)
    results = []

    for img_path, label in tqdm(pairs, desc="推論中"):
        try:
            result = client.predict(
                api_key=args.api_key,
                model_name=args.model,
                image=handle_file(str(img_path)),
                api_name=args.api_name
            )
            feats = parse_features_from_result(result)
            results.append({
                "label": label,
                "filename": str(img_path.relative_to(root)),
                "features_raw": str(result),
                "features": ";".join(feats)
            })
        except Exception as e:
            results.append({
                "label": label,
                "filename": str(img_path.relative_to(root)),
                "features_raw": f"ERROR: {e}",
                "features": ""
            })
        time.sleep(args.sleep)

    # 輸出每張圖結果
    df = pd.DataFrame(results)
    out1 = root / "results_per_image.csv"
    df.to_csv(out1, index=False, encoding="utf-8-sig")

    # 統計 (label × feature)
    exploded = []
    for r in results:
        feats = [x for x in r["features"].split(";") if x.strip()]
        for f in feats:
            exploded.append({"label": r["label"], "feature": f})
    df2 = pd.DataFrame(exploded)
    if not df2.empty:
        summary = (
            df2.groupby(["label", "feature"])
               .size()
               .reset_index(name="count")
               .sort_values(["label", "count"], ascending=[True, False])
        )
    else:
        summary = pd.DataFrame(columns=["label", "feature", "count"])
    out2 = root / "summary_by_label_feature.csv"
    summary.to_csv(out2, index=False, encoding="utf-8-sig")

    print(f"\n✅ 已完成分析：\n{out1}\n{out2}")

if __name__ == "__main__":
    main()
