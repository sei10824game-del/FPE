# FPE

Fundamental Paper Education と各 AU のキャラクターを追加する Minecraft 用ファン MOD です。

## プレイ環境

- Minecraft **1.20.1**
- Minecraft Forge **47.3.0**
- Java **17**

[Releases](https://github.com/sei10824game-del/FPE/releases/tag/latest) の `fpe-1.0.0.jar` を、上記 Forge 環境の `mods` フォルダーに入れてください。更新時は古い FPE の JAR を置き換えます。

## 開発・検証

Windows PowerShell:

```powershell
.\gradlew.bat build --no-daemon
.\gradlew.bat runGameTestServer --no-daemon
.\gradlew.bat preview -Pspec=miss_circle --no-daemon
```

Linux / macOS では `./gradlew` を使用します。初回は Forge などのダウンロードに時間がかかります。

- 配布用 JAR: `build/libs/fpe-1.0.0.jar`
- モデルとアニメーションのプレビュー: `build/preview/`
- 戦闘回帰テスト: `CombatGameTests`。陣営・攻撃者の所有関係、爆発、待機時間0の棘／罠／触手、遅延発動をサーバー上で検証します。失敗時は Gradle がエラー終了します。
- ゲームテストは開発用ワールドを生成します。普段遊んでいるワールドでの実行は不要です。

GitHub Actions は main への push と pull request でビルドと戦闘回帰テストを実行します。`latest` リリースの更新は、main の両方の検証が成功した場合に限ります。

## 引き継ぎ資料

- [現在の構成・制作手順](docs/HANDOFF_CHATGPT.md)
- [キャラクター制作 API](docs/CHARACTER_GUIDE.md)
- [ユーザーの制作ルールと確認済み資料](docs/HANDOFF.md)
- [身長](docs/HEIGHTS.md)

新しい攻撃には同名のアニメーションを用意し、攻撃の発生 tick と動作を合わせます。モデルを変更した場合はプレビュー画像を確認してください。見た目、クライアント描画、実戦のバランスは別途ゲーム内での確認が必要です。

## 今後の改善候補

- 拘束処理のジャンプ抑止を見直す。現在の Jump Boost amplifier 200 はジャンプを強化するため、移動同期も含めた修正とプレイヤーでの検証が必要です。
- 変身・掴み・連続攻撃の回帰テストを追加する。
- 確認済み資料を基準にシルエットと攻撃動作を改善し、ゲーム内で見え方を確認する。

ライセンスは [LICENSE.txt](LICENSE.txt) を参照してください。
