# A18 展示室2｜v02外周黒枠・左上通路（レビュー用／未採用）
2026-10-29

## 参照した実物
- `rooms/gallery2/architecture_only_v01.png`（展示室2の奥額縁2つを除去した930x582既存背景）
- `whole-museum-review/gallery2_approved_layout.png` と `rooms/gallery2/room.json`
- 展示室1の採用済み`gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png`
- `qa/architecture-bases-20261029/README.md`

## 今回の確認用処理
- **部屋の個性と元の壁・床の画像を残す**。展示室1の写真素材に置き換えない。
- 上端 y=0..15、下端 y=566..581 に黒枠、左と右の外周 x=0..43/x=886..929 に黒壁
- エントランスからの入口を**左上**の x=0..43,y=244..348 に開ける。展示室1右上開口を鏡写しにしたレビュー案。実ゲームでの移動位置検証は未実施
- 奥壁両端の柱は**元の展示室2の画像から**転用して内側へ配置
- 旧左手前の斜めの側面壁・右側の緑色側面壁は新しい四角い外枠に整合させる
- 左手前の既存床の不足部分は、同じ建築背景画像の開放済み床領域を鏡写しした画素で補う（新規描画・新規画像生成ではない）
- 奥の展示室4向けアーチは**従来のまま**、扉開閉の変更は行わない
- 既存の展示壁3台の座標、`room.json`、正式建築画像は変更なし

## 出力と検証
- `gallery2_v02_black_frame_left_upper_entrance_REVIEW.png` 930x582
- `gallery2_v01_vs_v02_black_frame_comparison_REVIEW.png`
- `qa/make_gallery2_v02_black_frame_review.py`で差分範囲、床中央、柱の画素一致、黒枠、開口判定などをassert。
- **監修前の候補**。workブランチでのみ保存し、issue/mainにはマージしない。ゲーム本体・試遊版も未変更。
