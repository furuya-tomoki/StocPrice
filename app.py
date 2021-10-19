import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title("株価可視化アプリ")

st.sidebar.write("""
# GAFA 株価
これは株価可視化ツールです。
以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider("日数", 1, 50, 20)


st.write(f"""
### 過去 **{days}日間**  のGAFA株価
""")


@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


try:
    st.sidebar.write("""
  ## 株価の範囲指定
  """)

    ymin, ymax = st.sidebar.slider(
        "範囲を選択してください。",
        0.0, 3500.0, (0.0, 3500.0)
    )
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

    companies = st.multiselect(
        "会社名を選択してください。",
        list(df.index),
        ["apple", "amazon", "google", "facebook"]
    )

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
