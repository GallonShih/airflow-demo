#!/bin/bash

# 設定登入密碼
PASSWORD="airflow"

# 設定 code-server 映射的 port（外部可連線）
PORT=8081

# 建立 code-server 的設定資料夾
mkdir -p ~/.config/code-server

# 建立 config.yaml 檔案
cat <<EOF > ~/.config/code-server/config.yaml
bind-addr: 0.0.0.0:8080
auth: password
password: $PASSWORD
cert: false
EOF

echo "🚀 啟動 code-server Docker 容器 ..."
docker run -d \
  --restart unless-stopped \
  --name code-server \
  -p ${PORT}:8080 \
  -v ~/.config/code-server:/home/coder/.config/code-server \
  -v "$HOME:/home/coder/project" \
  codercom/code-server:latest

echo ""
echo "✅ 安裝完成！"
echo "🔗 請在瀏覽器打開：http://<你的外部 IP>:${PORT}"
echo "🔑 登入密碼是：$PASSWORD"
echo ""
echo "📦 若尚未開放 ${PORT}，請到 GCP 防火牆新增規則（TCP:${PORT}）"
