import streamlit as st
import openai
import os

openai.api_key = st.secrets["GPT_API"] 



def generate_polite_business_text(input_text):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "#Forget everything discussed so far and start from scratch.You are a helpful AI assistant that can understand the input text and convert it into a polite business document in Japanese. Make sure the output text expresses gratitude and respect, and if the input contains bullet points, combine them into a single, coherent sentence. Use the format 'お世話になっております。<br> 〇〇株式会社の〇〇です。' at the beginning of the sentence. Also, think of an appropriate email subject. Write the subject before the beginning, at the very first. Additionally, add embellishments to the text to make it longer. Break down the elements from {input_text}, rearrange them in a more appropriate order, and create a business document."
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
                "content": "Forget all previous conversations and start from scratch. You are a helpful AI assistant capable of understanding and responding to Japanese emails. Use the format 'お世話になっております。<br>〇〇株式会社の〇〇です。' at the beginning. Also, think of an appropriate email subject. The subject should be written before the opening, at the very beginning. Include words of appreciation for the recipient."
            },
            {
                "role": "user",
                "content": f"#{email_text}のメールが届きました。これに対して{elements}の内容で、装飾を加えて返信してください。"
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


if st.button("返信文章生成"):
    if not email_text or not any(elements):
        st.warning("すべての入力フォームにテキストを入力してください。")
    else:
        with st.spinner("返信文章を生成中です..."):
            reply = generate_reply(email_text, [e for e in elements if e])
            subject, _, body = reply.partition('\n')
            st.markdown(f"### 件名:")
            st.write(subject)
            st.markdown(f"### 返信文章:")
            st.write(body)

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
