import streamlit as st
import requests
import json


st.header("Teacher App - Question Paper Generator")
st.divider()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True
# m = st.markdown("""
# <style>
# div.stButton > button:first-child {
#     background-color: #0099ff;
#     color:#ffffff;
# }
# div.stButton > button:hover {
#     background-color: #00ff00;
#     color:#ff0000;
#     }
# </style>""", unsafe_allow_html=True)
st.button('Generate Paper', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    try:
        reqUrl = "http://localhost/lang_chain_api/llm_call_with_prompt"

        headersList = {"Accept": "*/*","User-Agent": "Thunder Client (https://www.thunderclient.com)","Content-Type": "application/json"}

        template = """You are a school Teacher and you will generate question paper for assesment of seniour kg students.
        Generate question paper in following format example,

        Example:
        QUESTION-1: What comes After.<br />
        a) 14  _____ <br /><br />
        b) 7  _____ <br /><br /> 
        c) 10  _____ <br /><br />
        d) 55  _____ <br /><br /><br />

        QUESTION-2: What comes Before.<br /> 
        a) _____  13 <br /><br />
        b) _____  26 <br /><br /> 
        c) _____  65 <br /><br /> 
        d) _____  75 <br /><br /><br />

        QUESTION-3: In Between.<br /> 
        a) 11  _____  13 <br /><br /> 
        b) 24  _____  26 <br /><br /> 
        c) 65  _____  67 <br /><br /> 
        d) 77  _____  79 <br /><br /><br />

        QUESTION-4: Backward Counting.<br /> 
        a) 10  _____  8  7  _____  5  _____  3  2  _____ <br /><br />
        b) 7  _____  5  4  3  _____  _____ <br /><br /> 
        c) 20  19  _____  17  16  _____  14 <br /><br /> 
        d) 12  _____  10  _____  8  7  _____  5 <br /><br /><br />

        QUESTION-5: Skip Counting by 2.<br /> 
        a) 10  12  _____  16  18  _____ <br /><br />
        b) 5  7  _____  11  _____  15 <br /><br /> 
        c) 20  22  _____  _____  28  30 <br /><br /> 
        d) 72  74  _____  78  _____  82  84 <br /><br /><br />

        QUESTION-6: Addition.<br />
        a)<br />
            <span>&emsp;</span>4<br />
           +<br />
            <span>&emsp;</span>2<br />
        ------------<br /><br />

        b)<br />
            <span>&emsp;</span>22<br />
           +<br />
            <span>&emsp;</span>12<br />
        ------------<br /><br />

        QUESTION-7: Subtraction.<br />
        a)<br />
            <span>&emsp;</span>4<br />
           -<br />
            <span>&emsp;</span>2<br />
        ------------<br /><br />

        b)<br />
            <span>&emsp;</span>22<br />
           -<br />
            <span>&emsp;</span>12<br />
        ------------<br /><br />

        QUESTION-8: Write in words.<br /> 
        a) 10 _________________________________ <br /><br />
        b) 5  _________________________________ <br /><br /> 
        c) 20 _________________________________ <br /><br /> 
        d) 75 _________________________________ <br /><br /><br />
        
        Strictly follow below Instruction:
        - Generate questions in given format only but unique
        - Stick to given example only
        """

        payload = json.dumps({
        "template": template,
        "fields": {
        "field1": "Indian",
        "field2": "readymade cloths"
        },
        "model":"openai"
        })

        response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

        data = response['response']
        data = "<p><h4>"+str(data)+"</h4></p>"
        #data = "hello <br /> hello1 <br /> hello2"
        #st.write(data)
        st.markdown(data, unsafe_allow_html=True)
        st.session_state.clicked = False
    except:
        st.write("Try Again")
else:
    st.write("Click Button to generate Question Paper...")


#st.write(data)