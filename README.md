# 美股估值器

一个整合纳斯达克100、标普500估值和CNN恐惧贪婪指数的实时监控面板。

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
streamlit run app.py
```

## 部署到Google Cloud

1. 上传代码到GitHub
2. 在Google Cloud Run部署
3. 使用Dockerfile或Cloud Build自动构建

## 功能

- 📈 纳斯达克100 PE估值及历史分位
- 📊 标普500 PE估值及历史分位  
- 😱 CNN恐惧贪婪指数实时值
- 🌙 暗黑风格现代界面
- 🔄 手动刷新数据
