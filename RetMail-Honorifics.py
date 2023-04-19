import streamlit as st
import openai
import os

CHATGPT_API_KEY = st.secrets["GPT_API"]
openai.api_key = CHATGPT_API_KEY

def generate_polite_business_text(input_text):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "#Forget everything discussed so far and start from scratch.You are a helpful AI assistant that can understand the input text and convert it into a polite business document in Japanese. Make sure the output text expresses gratitude and respect, and if the input contains bullet points, combine them into a single, coherent sentence. Use the format 'お世話になっております。\n\n〇〇株式会社の〇〇です。' at the beginning of the sentence. Also, Additionally, add embellishments to the text to make it longer. Break down the elements from {input_text}, rearrange them in a more appropriate order, and create a business document."
            },
            {
                "role": "user",
                "content": input_text
            },
        ],
    )
    return res["choices"][0]["message"]["content"]

st.title("【ビジネス文章 作成】")

input_text = st.text_area("入力テキスト", "")

if st.button("文章変換"):
    if not input_text:
        st.warning("入力フォームにテキストを入力してください。")
    else:
        with st.spinner("ビジネス文章を生成中です..."):
            polite_business_text = generate_polite_business_text(input_text)
            st.markdown("### 生成されたビジネス文章:")
            st.write(polite_business_text)
            st.markdown('<a href="https://www.deepl.com/ja/translator" target="_blank" style="color:　Black;">英訳はこちらのDeeplをお使いください</a>', unsafe_allow_html=True)


# 水平線
st.markdown(
    """
    <div style="height: 3px; background-color: white; margin: 10px 0; border: none;"></div>
    """,
    unsafe_allow_html=True,
)

def generate_reply(email_text, elements):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Forget all previous conversations and start with a blank slate. You are an AI assistant who can understand Japanese emails and reply using 【Writing Techniques】. \
                    Use the format 「お世話になっております。\n\n〇〇株式会社の〇〇です。」 at the beginning of the 【reply content】 you create. Also, think of an appropriate email 件名. The 件名 should be written before the beginning. Include words of gratitude to the recipient.\
                        The contents of {elements} are the contents to be incorporated into the reply. Be careful not to write replies to {elements}.\
                【Writing Techniques】\
                [Polite language]: In written communication, polite language is important. Use honorifics and polite expressions to show consideration for the user.\
                [Clear and concise sentences]: Make your sentences clear and concise so that users can easily understand them. Avoid long sentences and jargon, and convey information using short and simple words.\
                [Open-ended questions]: To elicit information from users, ask open-ended questions. By asking questions that cannot be answered with Yes/No, you can obtain more information.\
                [Use affirmative words]: Use affirmative words to give users a sense of security. Choose words that accept the other person's feelings and situation and create a positive atmosphere.\
                [Soft expressions]: Use soft expressions to avoid giving users discomfort. Be mindful of polite expressions and seek information indirectly.\
                [Confirmation questions]: In communication with users, asking confirmation questions ensures that you can respond without misunderstandings. Ask appropriate questions to confirm that the information has been accurately conveyed.\
                [Appropriate compliments]: When users understand something or solve a problem, using appropriate compliments can create a positive atmosphere."
            },
            {
                "role": "user",
                "content": f"{email_text}の内容でメールが届きました。これに対して返信する文章【reply content】を作成してください。\
                #作成した【reply content】を分解し、分解した内容に{elements}の内容を追加してください。内容に相違があったところは{elements}の内容を上書きしてください。言葉が質問なのか、情報の伝達なのか、確認なのか意味をよく考えから上書きしてください。\
                #最終的に各項目ををお客様にわかりやすい順序で再構築して、【Writing Techniques】を使って箇条書きではない、一つのまとまった文章として書き出してください。\
                #文章が論理性で一貫性があるか考えておかしい点は{elements}を元に修正してください。\
                #必ず、最終結果の文章のみ表示してください。処理の途中を書き出すとあなたの評価が大きく下げられ不信感につながります。."
            },
        ],
    )
    return res["choices"][0]["message"]["content"]

st.title("【ビジネスメール 返信】")
st.write('<div id="header1" style="font-size:24px; font-weight:bold;">お客様へのメール文章 /</div>', unsafe_allow_html=True)
st.write('<div id="header2" style="font-size:24px; font-weight:bold;">返信に含める要素を入力してください。</div>', unsafe_allow_html=True)
st.write('<div id="header3" style="font-size:24px; font-weight:bold;">&nbsp;</div>', unsafe_allow_html=True)

email_text = st.text_area("お客様からのメール文章", "")
elements = [
    st.text_input("要素1", ""),
    st.text_input("要素2", ""),
    st.text_input("要素3", ""),
    st.text_input("要素4", ""),
]


if st.button("文章生成"):
    if not email_text or not any(elements):
        st.warning("すべての入力フォームにテキストを入力してください。")
    else:
        with st.spinner("返信文章を生成中です..."):
            reply = generate_reply(email_text, [e for e in elements if e])
            subject, _, body = reply.partition('\n')
            #st.markdown(f"### 件名:")
            st.markdown(f"<span style='font-size:18px; font-weight:bold;'>{subject}</span>", unsafe_allow_html=True)
            #st.markdown(f"### 返信文章:")
            st.write(body)
            st.markdown('<a href="https://www.deepl.com/ja/translator" target="_blank" style="color:　Black;">英訳はこちらのDeeplをお使いください</a>', unsafe_allow_html=True)


# グラデーション背景の追加
st.markdown(
    """
<style>
#header1, #header2, #header3 {
            margin-bottom: -20px !important;
        }
.stHeader {
    margin-bottom: -10px;
}
.stApp {
    background-color: #4158D0;
    background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stTextInput input {
    background-color: #FFFFFF;
    color: #000000;
}
.stButton>button:focus {
    outline: none;
}
</style>
""",
    unsafe_allow_html=True,
)
