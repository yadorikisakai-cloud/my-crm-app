import streamlit as st
import pandas as pd
import sqlite3
import datetime

# 1. データベース接続（なければ作成）
conn = sqlite3.connect('customer_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        contact_person TEXT,
        status TEXT,
        last_contact DATE
    )
''')
conn.commit()

# --- 画面構成 ---
st.title("簡易顧客管理システム (Internal CRM)")

# 2. サイドバー：新規登録フォーム
st.sidebar.header("新規顧客登録")
with st.sidebar.form("entry_form"):
    company = st.text_input("会社名")
    person = st.text_input("担当者名")
    status = st.selectbox("ステータス", ["見込み", "提案中", "契約済", "失注"])
    date = st.date_input("最終接触日", datetime.date.today())
    
    submitted = st.form_submit_button("登録")
    if submitted:
        c.execute("INSERT INTO customers (company_name, contact_person, status, last_contact) VALUES (?, ?, ?, ?)",
                  (company, person, status, date))
        conn.commit()
        st.sidebar.success("登録しました！")

# 3. メイン画面：データ一覧表示
st.header("顧客リスト")

# データベースから読み込み
df = pd.read_sql_query("SELECT * FROM customers", conn)

# 検索フィルター
search_query = st.text_input("会社名で検索")
if search_query:
    df = df[df['company_name'].str.contains(search_query)]

# データテーブル表示（編集可能にするなら st.data_editor もあり）
st.dataframe(df, use_container_width=True)

# 4. 簡易分析（ダッシュボード）
st.divider()
st.subheader("ステータス別件数")
st.bar_chart(df['status'].value_counts())