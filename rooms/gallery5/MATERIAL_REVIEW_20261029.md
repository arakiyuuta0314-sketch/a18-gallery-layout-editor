# A18 展示室5｜宮殿風E案・材質試作（採用待ち）

## 確認した正本とルール
- 共通 Git: `ios-app-starter/docs/GIT_WORKFLOW_COMMON.md`（2026-10-27 改訂版）。
- プレビューAGENTS: `AGENTS.md`。A18固有: `web-tools-preview/docs/DEVELOPMENT_GIT_POLICY.md`。
- 承認・引き継ぎ: `rooms/ARCHITECTURE_1_TO_4_HANDOFF_20261029.md`（issueの678bd88）、`rooms/gallery5/LAYOUT_E_APPROVAL_20261029.md`。
- 既存の実画像：`rooms/gallery5/gallery5_palace_E.png`、`rooms/gallery5/gallery5_palace_architecture_E.png`、展示室1〜4の採用画像。
- E案の方向性（宮殿風、3枠、ワインレッド、重厚な木材、控えめな金装飾、壁灯2灯、赤絨毯）は**既承認**。

## 試作したもの（**新しい材質案はどちらも未承認**）
- `qa/gallery5-material-20261029/gallery5_v01_material_architecture_REVIEW.png`：濃色ウォールナット系の柱・腰板、深いワインレッド壁紙、石調床、アーチ通路、赤絨毯。
- `qa/gallery5-material-20261029/gallery5_v02_material_architecture_REVIEW.png`：構造は同じで木柱を少し明るくして比較。
- 各 `*_3frame_mock_REVIEW.png` は中央の大作1枚と左右の縦額2枚を**仮で上に重ねた見た目だけ**。実作品を合成せず、額縁位置・大きさ・ゲーム設備IDを確定していない。
- `architecture-review/gallery5/index.html`：従来の採用Eラフとv01/v02、背景だけ・仮3枠ありをブラウザで比較できる。左右比較の境界を動かせる。
- `qa/make_gallery5_material_review.py` は元の研究画像に上書きせず、再生成可能。採用済み展示室4の床・壁の画素資料を参照して館内の材質連続性を確保し、暗色加工と独立した建築モチーフを構成。
- Web公開した場合も**監修プレビューであり正式採用ではない**。

## 変えないこと
- 部屋ID `gallery5`、南エントランス、西展示室3、東展示室4、北側には出口なし。
- 額縁数の決定（3枠）と旧ゲーム設備（5枠・全館28枠）の実装差分を混同しない。
- `rooms/gallery5/room.json`、ゲームソース、正式素材、当たり判定、進行Lv.6、保存スキーマは未変更。
- 不採用A〜D・F案、E案原本、展示室1〜4採用画像に上書きなし。mainおよびissueへの新案マージなし。

## QA
- `python qa/check_gallery5_material_preview.py`
- 画像930×582（比較画像は横2枚）、原Eとの差分確認。
- Chrome Headlessで1180pxと390px幅の画像読込、切替、スライダー、横はみ出しチェック。
- 通路の実ゲーム移動・collisionやキャラとの前後関係は未検証。採用後の別工程。
