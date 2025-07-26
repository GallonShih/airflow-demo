#!/bin/bash

# 設定密碼（可自行修改）
PASSWORD="airflow"

echo "🔧 安裝 code-server ..."
curl -fsSL https://code-server.dev/install.sh | sh

echo "🔐 設定登入密碼 ..."
mkdir -p ~/.config/code-server
cat <<EOF > ~/.config/code-server/config.yaml
bind-addr: 0.0.0.0:8081
auth: password
password: $PASSWORD
cert: false
EOF

echo "🎯 設定開機自動啟動（使用 systemd）..."
sudo systemctl enable --now code-server@$USER

echo ""
echo "✅ 安裝完成！"
echo "🔗 請在瀏覽器打開：http://<你的外部 IP>:8081"
echo "🔑 登入密碼是：$PASSWORD"
echo ""
echo "📦 若尚未開放 8081，請到 GCP 防火牆新增規則（TCP:8081）"
