# A18 展示室4｜西通路の柱状の張り出し v02 比較用（未採用）

## 指示・採否
2026-10-29：ユーザーから「アーチ付き通路いらない。普通の通路でいい。立体に見せようとしておかしくなってるので。」続いて「柱状の張り出しだけ見たいから作って欲しい」と指定。

- **柱なし** v01：`gallery4_v01_plain_west_passage_architecture_REVIEW.png`、通常の左側黒枠の開口 x0..43 y294..426。
- **柱あり** v02：`gallery4_v02_west_attached_column_REVIEW.png`、v01に西側通路の内側端 x44..86 y237..445へ**柱状の出っ張り1本だけ**を追加。木の足元とクリーム色の柱面は展示室1の既存素材を転用。アーチ・扉・大きい側面壁は追加しない。
- v02は形状検討専用。**採用済みとは扱わない**。ユーザーの比較判断を待つ。

## 保持する条件
- 展示室4：A案の奥壁四枠（縦、横、縦、横）＋独立壁⑤一枠、合計五枠。
- `rooms/gallery4/room.json`、正本`architecture_only_A.png`、`gallery4_A_rear.png`、独立展示壁の位置 (614,323,210,165) に変更なし。
- 南中央は展示室2への通路、右壁は閉鎖、左は展示室5への通路。
- 変更がv01からx42..92 y236..447に限定されること、左の床続き通路、南中央の開口、右壁、奥壁は不変であることを画素比較で検証。
- ゲームの歩行、当たり判定、レイヤー、開放条件は未検証。今回のQAは画像のQAのみ。

## 出力
- `qa/make_gallery4_v01_architecture_review.py`：v01基準画像を再現。新規作業で生成し、元の承認アセットは不変。
- `qa/make_gallery4_v02_single_column_projection.py`：v02画像、A案五枠重ね画像、左右比較画像、左通路拡大画像、両正本SHA不変検証。
- `gallery4_v02_west_attached_column_REVIEW.png`：建築背景のみ。
- `gallery4_v02_attached_column_approved_A_five_frames_REVIEW.png`：独立壁のレイアウト確認用。
- `gallery4_v01_plain_vs_v02_column_COMPARISON.png` と `gallery4_v01_v02_west_column_detail_COMPARISON.png`：比較。
- `architecture-review/gallery4/index.html`：スマホ／PCで「柱あり・柱なし・スライダー比較」と拡大を閲覧。

統合：`work/a18-architecture-bases-20261029`にのみ保存、issue/mainにはマージしない。正式ゲームへの組み込み・公開も行わない。未追跡の他ユーザー作業9件は保持する。
