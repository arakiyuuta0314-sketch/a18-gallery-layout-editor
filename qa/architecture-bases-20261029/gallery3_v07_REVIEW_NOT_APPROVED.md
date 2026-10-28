# A18 展示室3 建築背景 v07｜元の黒くない壁面素材に合わせる（未承認）

## ユーザーの修正指示
- 「白すぎる。。。壁の素材の黒じゃない方って意味でした…」
- 以前のv06は白い柱から色を取って白壁と誤認した。**正解は元の凹み側面素材の黒い影ではない側**であり、白く塗りつぶすことではない。

## 参照元の実画素と変更内容
- 元画像：`gallery3_v04_completed_side_cornices_lowered_east_passage_REVIEW.png`
- 左の黒くない壁面：原画x290..293, y57..144（茶灰色 約RGB 123,103,79）
- 右の黒くない壁面：原画x657..660, y57..144（茶灰色 約RGB 114,95,73）
- 黒い影の帯 x279..285／x665..671 は**参照せず**、白い柱の画素も参照しない。
- 上記素材の微細な陰影をそのまま伸長・遠近変換して左右凹み側面（左x269..295、右x655..680）へ入れた。読みやすさのため露出のみ約10%上げ、純白にはしない。
- v06をベースに**左右側面以外は画素を一切変更していない**。凸形の黒枠、奥壁、通路（東x886..929,y294..426）、下中央入口、他の床・壁、展示枠5枚の配置に変更なし。

## 出力・QA
- スクリプト：`qa/make_gallery3_v07_nonblack_wall_faces.py`、各側面実素材の出所と変更許可範囲のピクセルassert付き。
- 原寸：`gallery3_v07_existing_nonblack_wall_material_REVIEW.png` 930×582
- 全体比較：`gallery3_v06_v07_actual_wall_material_COMPARISON.png`
- 側面拡大：`gallery3_v07_niche_material_closeup_COMPARISON.png`
- Web確認：`architecture-review/gallery3/index.html`（v07とv06の切替・左右比較・拡大）
- 承認前の候補。正式ゲームアセット、room.json、ゲーム本体や通行判定は変更していない。**issue/main統合もしない**。
