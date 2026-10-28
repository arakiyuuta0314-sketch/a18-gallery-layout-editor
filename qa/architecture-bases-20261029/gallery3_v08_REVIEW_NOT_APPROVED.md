# A18 展示室3 v08｜側面の下部木製腰板・柱側面の立体感（監修待ち）
2026-10-29

## 今回の依頼
- 「側面の下部を壁と同じく木の材質にして、柱部分の立体感は必要」
- v07の凸型形状と灰茶色の上部側面はそのまま。左右の凹み側面の下部のみ正面と同じ木製腰板へ。
- 凹みの手前の柱が平板にならないよう、既存柱の側面木製モール材を細い遠近の面として追加し、上端と足元には細い境界線を配置。

## 画像・出典
- v07: `qa/architecture-bases-20261029/gallery3_v07_existing_nonblack_wall_material_REVIEW.png`
- 実木材: `qa/architecture-bases-20261029/gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png` の腰板x116..214,y166..218
- 柱の側面: 展示室1 v13 `gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png` の柱木製モールx478..482,y39..219
- 凹みの側面：左x269..295（y81から前面、y39から後面）、右x655..680。腰板の上端は前面y約210、後面y約140に沿って斜めに接続。
- 実素材の遠近投影のみで構成。新しい独立展示柱・扉・棚などは追加しない。
- 元画像の室内床、凸型黒枠、右側出口、下中央入口、中央奥壁、承認済み展示枠の座標やゲーム実装は変更しない。

## QAと状態
- `qa/make_gallery3_v08_wood_lower_returns.py` で同じ既存素材を再生成、変更画素が左右側面2か所に収まることと、他の部屋・通路・床が無変更なことをassert。
- 画像930×582: `gallery3_v08_wood_lower_returns_3d_columns_REVIEW.png`
- 全体比較: `gallery3_v07_v08_wood_lower_returns_COMPARISON.png`
- 拡大比較: `gallery3_v08_wood_sidewalls_detail_COMPARISON.png`
- Webプレビュー: `architecture-review/gallery3/index.html`（v08/v07の切替・スライダー・拡大比較）
- **まだユーザー監修前**。作業ブランチにのみ保存し、課題/mainへマージしない。ゲーム本体や正式画像・通行判定は未変更。
