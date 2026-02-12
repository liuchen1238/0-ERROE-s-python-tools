# 0-ERROE-s-python-tools

這個倉庫包含一些 Python 工具。以下為 `pip_module_manager.py` 的使用說明。

## pip_module_manager.py

這個工具提供兩個主要功能：

- **列出當前環境已安裝的 pip 套件**：

  ```bash
  python pip_module_manager.py list
  ```

  執行上面命令會列出已安裝套件的名稱及版本。

- **下載指定套件的分發檔**：

  ```bash
  python pip_module_manager.py download [套件名稱[==版本]] [--dir 下載目錄]
  ```

  `download` 子命令會使用 `pip download` 將指定套件下載至目標資料夾，預設為當前目錄。

  例如下載 `requests` 套件到 `/tmp/downloads`：

  ```bash
  python pip_module_manager.py download requests --dir /tmp/downloads
  ```

  若需指定版本，可在套件名稱後加上 `==版本號`。

此外，`pip_module_manager.py` 在檔案開頭包含 `#!/usr/bin/env python3` 的 shebang，並且在底部定義了 `if __name__ == "__main__": main()`，因此將檔案設為可執行（`chmod +x pip_module_manager.py`）後，即可在 Bash 直接執行，例如：

```bash
./pip_module_manager.py list
./pip_module_manager.py download requests --dir /tmp/downloads
```

這個工具採模組化設計，各函式可在其他程式中重複使用。

## 其他常用的 Python 開發工具

除了 `pip_module_manager.py`，Python 開發還常會用到以下工具來解決各種開發問題：

- **`black`** — 程式碼自動格式化工具，可依照 PEP 8 標準統一程式碼的樣式。
- **`ruff` 或 `flake8`** — 程式碼靜態檢查工具，用於找出未使用的變數、不當語法等潛在錯誤。 `ruff` 效能較好且提供多種檢查規則集成。
- **`mypy`** — 靜態類型檢查工具，支援 PEP 484 類型標準，可在執行前發現類型不一致的問題。
- **`pytest`** — 強大的測試框架，提供簡潔的語法、fixture 模組及豐富的插件，用於撰寫與執行單元測試。
- **`pre-commit`** — Git 預提交掛銀管理工具，可在提交前自動執行 linter/格式化檢查，確保提交品質。
- **`poetry` 或 `pipenv`** — 依豆與虛擬環境管理工具，簡化工程的套件安裝、版本鎖定及發佈流程。
- **`isort`** — 自動整理 import 項帳，方便在项目中保持一致的安排和分類，常與 `black` 配合使用。
- **`coverage`** — 認證測試覆蓋率的工具，可與 `pytest` 整合使用来評估測試是否適當。
- **`bandit`** — 安全靜態分析工具，用來掃描 Python 碼中的可能安全脈碎和缺陷。
- **`pudb`** — 文字界面的人性化除錯器，提供全螢幕交互式的掛可視化堆籤與變數管理功能。
- **`Sphinx`** — 文件生成工具，可從程式碼製生 API 文件，支援 reStructuredText 或 Markdown 格式。
