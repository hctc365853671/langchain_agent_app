from agent import Agent
import streamlit as st
import os


#---------------app----------- 
st.title("产品智能助手")
if "agent" not in  st.session_state:
    st.session_state.agent=Agent()
if "messages" not in st.session_state:
    st.session_state.messages=[]
if "file_statu" not in st.session_state:
    st.session_state.file_statu=False
if "pdf_temp" not in st.session_state:
    st.session_state.pdf_temp=None
if "all_pdf_name" not in st.session_state:
    st.session_state.all_pdf_name=[]
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  
#侧边栏
with st.sidebar:
    st.title("智能助手使用说明")
    st.markdown("# 📖 使用说明")
    st.divider()
    st.markdown("""
    - 🌤️ **天气查询**
      提问包含城市+天气，会返回天气卡片
      > 示例：鄂州今天天气怎么样？
    - 📦 **产品咨询**
      提问产品相关，返回产品介绍卡片
      > 示例：投影仪参数、投影仪怎么选
    - ✅ 操作
      1. 在输入框输入问题
      2. 点击【发送】获取回答
      3. 点击【清空对话】清空回答内容
    """)
    st.divider()
    st.markdown("💡 提示：一次只提一个问题，识别更准确")
#页面分区-----------------
col_chat,col_history= st.columns([6,4])
with col_chat:
    #文件上传------------
    up_pdf=st.file_uploader("上传PDF拓展知识库",type=["pdf"],max_upload_size=10,disabled=st.session_state.file_statu,key=st.session_state.uploader_key)
    if up_pdf:
        st.session_state.file_statu=True
        st.session_state.pdf_temp=up_pdf
        st.session_state.uploader_key+=1
        st.rerun()
    if st.session_state.pdf_temp and st.session_state.pdf_temp.name not in st.session_state.all_pdf_name:
        mir="./upload"
        if not os.path.exists(mir):
            os.mkdir(mir)
        save_patt=os.path.join(mir,st.session_state.pdf_temp.name)
        st.session_state.pdf_temp.seek(0)
        with open(save_patt,"wb") as f:
            f.write(st.session_state.pdf_temp.read())
        issucc=st.session_state.agent.pdf_to_embedding(save_patt)
        if issucc:
            st.session_state.all_pdf_name.append(st.session_state.pdf_temp.name)
            st.success("添加成功")
        else:
            st.warning("添加失败")
        st.session_state.file_statu = False
        st.session_state.pdf_temp = None
        st.rerun()
    st.write("已添加:")
    for name in st.session_state.all_pdf_name:
        st.write(name)
    #中间问答界面-----------------
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("请输入您的问题或需求", height=100)
        send_button = st.form_submit_button("发送")
        # ========== 表单区域 end ==========
        if send_button:
            ai_answen_content=st.session_state.agent.response(user_input)
            st.success(ai_answen_content)
            st.session_state.messages.append({user_input:ai_answen_content})
    #-------清空按钮-------------
    clear=st.button("清空记录")
    if clear:
        st.session_state.agent.messages=[]
        st.session_state.messages=[]
        st.rerun()
    #--------------------
#历史记录展示            
with col_history:
    for mes in  st.session_state.messages:
        for u,a in mes.items():
            st.write(f"用户提问:{u}")
            st.write(f"ai回答:{a}")

    