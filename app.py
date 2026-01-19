import streamlit as st
import time

# ==========================================
#  デザイン設定（CSS）
# ==========================================
st.markdown("""
    <style>
    /* --- 音声プレイヤーを隠す設定 --- */
    .stAudio {
        display: none;
    }

    /* ============================================================
       右側のボタンエリアのデザイン
       ============================================================ */
    
    /* 1. 再生ボタン（上段・青） */
    div[data-testid="column"]:nth-of-type(2) > div > div > div > div > div.stButton > button {
        background-color: #0068c9 !important;
        color: white !important;
        border: none;
        height: 70px;
        font-size: 22px !important;
        font-weight: bold;
        width: 100%;
        margin-bottom: 300px !important; /* ボタン間の間隔300px */
    }
    div[data-testid="column"]:nth-of-type(2) > div > div > div > div > div.stButton > button:hover {
        background-color: #0052a3 !important;
    }

    /* 2. はいボタン（下段左・水色・超巨大） */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-of-type(1) button {
        background-color: #00b4d8 !important;
        color: white !important;
        border: none;
        height: 300px !important; /* 高さ300px */
        font-size: 40px !important;
        font-weight: bold;
        width: 100%;
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-of-type(1) button:hover {
        background-color: #0096c7 !important;
    }

    /* 3. いいえボタン（下段右・赤・超巨大） */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-of-type(2) button {
        background-color: #ff6b6b !important;
        color: white !important;
        border: none;
        height: 300px !important; /* 高さ300px */
        font-size: 40px !important;
        font-weight: bold;
        width: 100%;
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-of-type(2) button:hover {
        background-color: #ee5253 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
#  設定エリア
# ==========================================

# --- オマケ時間の設定 ---
EXTRA_TIME = 4.0

# --- 画像の設定 ---
TALKING_GIF = "talking_loop.gif"
SILENT_PNG = "silent_face.png"
IMG_WIDTH = 450 

# --- 音声ファイルと質問文のリスト ---
START_DATA = {"file": "audio/00_start.mp3", "duration": 8.0}
END_DATA   = {"file": "audio/99_end.mp3",   "duration": 7.2}

questions = [
    {"text": "固くしまった瓶のふたを開けるのは、困難ですか？", "file": "audio/01_bin.mp3", "duration": 3.73},
    {"text": "ペンで文字を書くのは、困難ですか？", "file": "audio/02_kaku.mp3", "duration": 2.66},
    {"text": "鍵を回すのは、困難ですか？", "file": "audio/03_kagi.mp3", "duration": 2.13},
    {"text": "食事の支度をするのは、困難ですか？", "file": "audio/04_ryouri.mp3", "duration": 2.92},
    {"text": "重いドアを押して開けるのは、困難ですか？", "file": "audio/05_door.mp3", "duration": 2.89},
    {"text": "重い物を、棚の上に置くのは、困難ですか？", "file": "audio/06_tana.mp3", "duration": 2.77},
    {"text": "壁拭きや床磨きなど、重い家事をするのは、困難ですか？", "file": "audio/07_kaji.mp3", "duration": 3.27},
    {"text": "庭仕事や、農作業をするのは、困難ですか？", "file": "audio/08_niwa.mp3", "duration": 3.43},
    {"text": "ベッドメイクをするのは、困難ですか？", "file": "audio/09_bed.mp3", "duration": 2.4},
    {"text": "買い物袋や、カバンを持つのは、困難ですか？", "file": "audio/10_bag.mp3", "duration": 3.28},
    {"text": "5キロ程度の重い荷物を持つのは、困難ですか？", "file": "audio/11_omoi..mp3", "duration": 2.79},
    {"text": "頭上の電球を替えるのは、困難ですか？", "file": "audio/12_denkyu.mp3", "duration": 2.95},
    {"text": "髪を洗ったり、ドライヤーをかけるのは、困難ですか？", "file": "audio/13_kami.mp3", "duration": 3.16},
    {"text": "背中を洗うのは、困難ですか？", "file": "audio/14_senaka.mp3", "duration": 2.46},
    {"text": "セーターやトレーナーを着る動作は、困難ですか？", "file": "audio/15_fuku.mp3", "duration": 3.01},
    {"text": "ナイフを使って食事をするのは、困難ですか？", "file": "audio/16_knife.mp3", "duration": 3.11},
    {"text": "カードや編み物など、衝撃の少ない趣味の活動は、困難ですか？", "file": "audio/17_rec_light.mp3", "duration": 3.79},
    {"text": "テニスやゴルフなど、手を使うスポーツ活動は、困難ですか？", "file": "audio/18_rec_heavy.mp3", "duration": 3.3},
    {"text": "車を運転するなど、自分の手段で移動するのは、困難ですか？", "file": "audio/19_ido.mp3", "duration": 3.47},
    {"text": "性生活に、肩や腕のせいで問題はありますか？", "file": "audio/20_sei.mp3", "duration": 3.12},
    {"text": "家族や友人、近所付き合いなどの社会活動は、困難ですか？", "file": "audio/21_shakai.mp3", "duration": 3.30},
    {"text": "腕や手の問題のせいで、付き合いや趣味などの社会活動に障害がありましたか？", "file": "audio/22_shogai.mp3", "duration": 7.11},
    {"text": "腕や手の問題のせいで、仕事や普段の活動が制限されましたか？", "file": "audio/23_seigen.mp3", "duration": 4.57},
    {"text": "腕、肩、手に、痛みはありますか？", "file": "audio/24_itam.mp3", "duration": 3.48},
    {"text": "活動した時の、腕、肩、手の痛みは強いですか？", "file": "audio/25_itami_act.mp3", "duration": 3.86},
    {"text": "しびれや、ピリピリ感はありますか？", "file": "audio/26_shibire.mp3", "duration": 2.78},
    {"text": "腕、肩、手の脱力感、つまり力が入りにくい感じはありますか？", "file": "audio/27_datsuryoku.mp3", "duration": 4.12},
    {"text": "腕、肩、手のこわばりはありますか？", "file": "audio/28_kowabari.mp3", "duration": 2.83},
    {"text": "痛みで眠れないなど、睡眠に影響はありますか？", "file": "audio/29_suimin.mp3", "duration": 4.22},
    {"text": "腕や手の問題のせいで、自分を役に立たないと感じたり、自信をなくしたりしていますか？", "file": "audio/30_jishin.mp3", "duration": 5.28},
]


# ==========================================
#  アプリ本体の処理
# ==========================================

if 'q_index' not in st.session_state:
    st.session_state.q_index = 0 
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'last_played_idx' not in st.session_state:
    st.session_state.last_played_idx = -1

st.title("DASHスコア問診アプリ")

# --- 1. 挨拶ページ ---
if st.session_state.q_index == 0:
    st.subheader("ご案内")
    st.write("▼ 看護師がご案内します")

    c_img, c_btn = st.columns([1.5, 1], vertical_alignment="center")
    
    with c_img:
        image_spot = st.empty()
        image_spot.image(SILENT_PNG, width=IMG_WIDTH)
    
    with c_btn:
        if st.button("▶ 問診を開始する", type="primary"):
            audio_box = st.empty()
            image_spot.image(TALKING_GIF, width=IMG_WIDTH)
            
            # ★変更点: 現在時刻を使って「key」を毎回新品にする
            unique_key = f"start_{time.time()}"
            audio_box.audio(START_DATA['file'], autoplay=True, key=unique_key)
            
            with st.spinner("挨拶中..."):
                time.sleep(START_DATA['duration'] + EXTRA_TIME) 
            image_spot.image(SILENT_PNG, width=IMG_WIDTH)
            time.sleep(1.0) 
            st.session_state.q_index = 1
            st.rerun() 
    
    st.write("---")

# --- 2. 終了ページ ---
elif st.session_state.q_index > len(questions):
    st.subheader("診断終了")
    c_img, c_btn = st.columns([1.5, 1], vertical_alignment="center")
    with c_img:
        image_spot = st.empty()
        image_spot.image(SILENT_PNG, width=IMG_WIDTH)
        audio_box = st.empty()

    if st.session_state.last_played_idx != st.session_state.q_index:
        with st.spinner("（1秒後に終了の挨拶が始まります...）"):
            time.sleep(1.0)
        image_spot.image(TALKING_GIF, width=IMG_WIDTH)
        
        # 自動再生
        audio_box.audio(END_DATA['file'], autoplay=True, key="end_auto")
        
        with st.spinner("お話中..."):
            time.sleep(END_DATA['duration'] + EXTRA_TIME)
        image_spot.image(SILENT_PNG, width=IMG_WIDTH)
        st.session_state.last_played_idx = st.session_state.q_index

    with c_btn:
        if st.button("▶ もう一度挨拶を聞く", type="primary"):
            image_spot.image(TALKING_GIF, width=IMG_WIDTH)
            
            # ★変更点: keyを毎回変える
            unique_key = f"end_retry_{time.time()}"
            audio_box.audio(END_DATA['file'], autoplay=True, key=unique_key)
            
            with st.spinner("お話中..."):
                time.sleep(END_DATA['duration'] + EXTRA_TIME)
            image_spot.image(SILENT_PNG, width=IMG_WIDTH)
        
    st.success(f"お疲れ様でした！すべての回答が終わりました。\n\n**あなたのDASHスコア換算値：{st.session_state.score}**")
    st.write("---")
    if st.button("最初に戻る"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()

# --- 3. 質問ページ ---
else:
    q_data = questions[st.session_state.q_index - 1]
    st.subheader(f"Q{st.session_state.q_index}. {q_data['text']}")
    c_img, c_btn = st.columns([1.5, 1], vertical_alignment="center")

    with c_img:
        image_spot = st.empty()
        image_spot.image(SILENT_PNG, width=IMG_WIDTH)
        audio_box = st.empty()

    with c_btn:
        if st.button("▶ もう一度質問を聞く", type="primary", key=f"replay_btn_{st.session_state.q_index}"):
            image_spot.image(TALKING_GIF, width=IMG_WIDTH)
            
            # ★変更点: keyを毎回変える（これでWebでも動きます！）
            unique_key = f"q_{st.session_state.q_index}_{time.time()}"
            audio_box.audio(q_data['file'], autoplay=True, key=unique_key)
            
            with st.spinner("読み上げ中..."):
                time.sleep(q_data['duration'] + EXTRA_TIME)
            image_spot.image(SILENT_PNG, width=IMG_WIDTH)

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            if st.button("はい", use_container_width=True):
                st.session_state.score += 5
                st.session_state.q_index += 1
                st.rerun()
        with sub_c2:
            if st.button("いいえ", use_container_width=True):
                st.session_state.score += 0
                st.session_state.q_index += 1
                st.rerun()

    st.write("---")

    if st.session_state.last_played_idx != st.session_state.q_index:
        time.sleep(1.0)
        image_spot.image(TALKING_GIF, width=IMG_WIDTH)
        
        # 自動再生
        unique_key = f"auto_q_{st.session_state.q_index}"
        audio_box.audio(q_data['file'], autoplay=True, key=unique_key)
        
        with st.spinner("読み上げ中..."):
            time.sleep(q_data['duration'] + EXTRA_TIME)
        image_spot.image(SILENT_PNG, width=IMG_WIDTH)
        st.session_state.last_played_idx = st.session_state.q_index
