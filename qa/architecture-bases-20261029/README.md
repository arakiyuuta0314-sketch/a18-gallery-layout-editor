# A18 建築背景のみ候補（2026-10-29）— ユーザー監修待ち

## 正本
- 各展示室の正式な構成は `rooms/galleryN/room.json`、承認済み視覚記録は `whole-museum-review/galleryN_approved_layout.png`。
- 背景の確認候補は**原画像・room.json の置換ではない**。画像に焼き込まれていた奥の額縁だけを除く。
- 独立展示壁・案内台・スタッフ・当たり判定は制作・統合対象外。作品枠・セーブ・進行の変更は禁止。

| 室 | 建築のみの候補 | 除去した奥の枠数 | 比較画像 |
| --- | --- | ---: | --- |
| 2（A） | `rooms/gallery2/architecture_only_v01.png` | 2 | `gallery2_before_after.png` |
| 3（G） | `rooms/gallery3/gallery3_architecture_only_E.png`（既存原本をそのまま使用） | 3 | `gallery3_before_after.png` |
| 4（A） | `rooms/gallery4/architecture_only_A.png`（既存原本をそのまま使用） | 4 | `gallery4_before_after.png` |
| 5（E） | `rooms/gallery5/gallery5_palace_architecture_fixed_E_v01.png` | 3 | `gallery5_before_after.png` |

## 検証
- すべて 930×582。承認済みの壁・床・柱・出入口・遠近・固定装飾は保持。
- 生成スクリプト `qa/make_gallery2_architecture_base.py` と `qa/make_gallery345_architecture_bases.py` は、額縁範囲外の**全画素一致**を検査する。差分は除去した額縁の矩形内に限る。
- 展示室2の壁面再構築は生成元 `qa/build_gallery2_editor.py` の実際の塗り色 `#214e43` を再使用。全体画像再生成・推測補完なし。
- 展示室3と4の建築原本は既存の承認済み作業ソースに存在するため新規加工なし。
- 展示室5は元のE案生成コード `qa/gallery5_palace_EF.py` の承認済み壁灯・カーテンを既存の建築原本に同一手順で描き、額縁だけ省略。
- `gallery2_qa.json` と `gallery345_qa.json` に参照元・SHA-256・画素差分範囲を保存。
- 回帰検証：check_editor, check_reuse, check_gallery1_v07, check_gallery2_concepts, check_gallery2_live, check_gallery3_live, check_gallery4_live, check_gallery5_live, check_whole_museum_review の9系統PASS（PC幅1180・スマホ幅390を含む）。

## 監修・実装ゲート
- **現在：ユーザーの背景確認待ち**。建築背景のみ4室の採否が決まるまでゲームへの組み込みへ進まない。
- `room.json` の参照先は既存承認レイアウトのまま維持。
- `web-tools-preview`（ゲーム本体）は未改修。保存v3・gallery5の5枠→3枠移行も保留（計26枠は決定済み、現行ゲーム28枠のまま）。
- work→issueのマージ、main更新、試遊版の公開は、明示許可まで禁止。
