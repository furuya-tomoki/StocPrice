 # データ解析ライブラリ
 # DataFrameなど使用可能
import pandas as pd
 # 株価情報の取得が可能
import yfinance as yf
 # 散布図を作成するライブラリ
import altair as alt
 # streamlitに反映するライブラリ
import streamlit as st

 # サイトのタイトル
st.title("株価可視化アプリ")

 # サイトのサイドバー
 # マークダウンで記述
st.sidebar.write("""
# GAFA 株価
これは株価可視化ツールです。
以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")
 # slider = スライダーツールの作成
 # （"タイトル",最小値, 最大値, デフォルト値）
 # 変数daysに代入
days = st.sidebar.slider("日数", 1, 50, 20)

 # f = 文字列の一部に変数や式をいれておき、それを実行時に置き換えるというもの
 # daysには、("日数", 1, 50, 20)が代入されている
st.write(f"""
### 過去 **{days}日間**  のGAFA株価
""")

 # 読み取り速度を向上してくれる
@st.cache 
 # 関数名get_data(引数1=days, 引数2=tickers)
def get_data(days, tickers):
   # 変数df = DataFrame
    df = pd.DataFrame()
    # for文 「company」の中に「tickersのキー」1つずつ代入
    for company in tickers.keys():
      # 変数tkrにはyfinanceが反映
        tkr = yf.Ticker(tickers[company])
         # history = 過去の情報
         # period = 日付を Period として扱う
         # d = dを用いることで数値を文字列中に代入
        hist = tkr.history(period=f'{days}d')
         # index = 要素がlistの中で何番目かを示すもの
         # strftime() = 任意のフォーマットの文字列に変換
        hist.index = hist.index.strftime('%d %B %Y')
         # 「Close」カラムを指定
        hist = hist[['Close']]
         # カラムを「company」の値に変更
        hist.columns = [company]
         # T = データを横に変換
        hist = hist.T
         # index.name = データフレームindexとcolumnsのタイトル
        hist.index.name = 'Name'
         # cancat = 複数のpandas.DataFrame, pandas.Seriesを連結する
         # このばあい、「dfとhist」が連結している
        df = pd.concat([df, hist])
    return df

 # エラーが起きた時に、以下の処理が行われる
try:
    st.sidebar.write("""
  ## 株価の範囲指定
  """)
    ymin, ymax = st.sidebar.slider(
        "範囲を選択してください。",
        0.0, 3500.0, (0.0, 3500.0)
    )
     # tickersの中のデータ
    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN',
        'Twitter': "TWTR",
        'Accenture A': 'ACNB',
        'キャノン株式会社': 'CAJ',
        '本田技研工業株式会社': 'HMC',
        'オリックス株式会社': 'IX',
        'くら寿司 USA': 'KRUS',
        '株式会社みずほフィナンシャルグループ': 'MFG',
        '株式会社三菱UFJフィナンシャル・グループ': 'MUFG',
        'ソニーグループ株式会社': 'SONY',
        'トヨタ自動車株式会社': 'TM',
        '野村ホールディングス株式会社': 'NMR'
    }
    df = get_data(days, tickers)

     # multiselect = マルチセレクト機能の追加（複数選択）
    companies = st.multiselect(
        "会社名を選択してください。",
        list(df.index),
        ["apple", "amazon", "google", "facebook"]
    )

     # if文 = 選択されなかった場合の処理
    if not companies:
        st.error("少なくとも一社は選んでください。")
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["Date"]).rename(
            columns={"value": "Stock Prices(USD)"}
        )

    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None,
                    scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )

    st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        "エラーが起きているようです！"
    )
