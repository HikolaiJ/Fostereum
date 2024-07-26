#Libraries
import streamlit as st
from PIL import Image
#from streamlit_javascript import st_javascript
from streamlit.components.v1 import html
import base64
import pandas as pd
import pickle

favic = Image.open("etc/ikon.ico")
st.set_page_config(page_title="Fostereum", page_icon=favic, initial_sidebar_state="collapsed")
plc = st.empty()
#pickle.load(open("etc/redderick_model.pkl", "rb"))

with open ("etc/script.js") as f:
    jz=f.read()

#Native Contents
def main():
    picLogo = open("etc/ikon.png", 'rb')
    pr_picLogo= base64.b64encode(picLogo.read()).decode("utf-8")
    picLogo.close()
    plc.html(f"""
        <div id="CONT" pageState="Homepage">
        <div id="HomeIcon" class="centers">
            <button id="LogoBut" style="box-shadow:#000000bd 0px 0px 13px 16px;"><img class="centers" style="padding:20px; padding-right:40px; width:100%;" src="data:image/gif;base64,{pr_picLogo}"/></button>
            <p class="centers" style="padding:0;text-shadow:#8e8e8e 7px 5px 10px;color:white;padding-right:35px;width:350px;text-align:center;font-size:57px;font-weight:700;">FOSTEREUM</p>
        </div>
        </div>
    """)
    html(f"<script>{jz}</script>")

#External Contents
def page1():
    plc.html("""
            <div id="CONT" pageState="camerasection">
             <div id="display-cam" class="ection" style="background:#222222;width:765px;height:402px;"></div>
             <div id="content-control" class="ection" style="background:white;width:765px;height:200px;margin-top:20px;box-shadow:inset #00000040 0 0 15px 4px;"></div>
            </div>
        """)
    html(f"<script>{jz}</script>")
def page2(): # show prediction and data of sensors
    plc.html(f"""
            <div id="CONT" pageState="graphic-sensors>
             <div class="ection" id="LineGraph-res" style="background:white; width:753px; height:400px; margin-left:-140px; display:inline-block;"></div>
             <div class="ection" id="Sensors-det" style="background:#dcffc8; width:250px; height:400px; display:inline-block; margin-left:17px; position:absolute;"></div>
             <div class="ection" id="data-logs" style="background:gray; width:1020px; height:207px; margin-left:-140px;margin-top:12px;">tes huruf cuy -</div>
            </div>
        """)
    """
    plc.line_chart(Redderick.predict(pd.read_csv("etc/25-07-24 Dataset 1.csv")))
    with open ("etc/scr_p2.js") as f:
        html(f"<script>{jz}{f.read()}</script>")
"""
def settingsP():
    plc.html("""
<div id="CONT" pageState="setting" style="margin-left:-76px; padding:0px 31px; background:rgb(210, 247, 214); height:600px; width:900px; border-radius:13px; box-shadow:inset #00000091 0 0 30px 7px;">
    <h1>Settings</h1>
    <div id="Telegram-id">
        <label>Telegram Chat ID</label><input style="border-radius:9px;">
    </div>
    <div id="bot-feature">
        <label>Weekly report</label>
        <br>
        <label>Alert when plant's environment is not suitable</label>
    </div>
</div>
""")


#Start web
if __name__ == "__main__":
    with open ("etc/style.css", "r") as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
    settingsP()
    if st.sidebar.button("Home"):
        main()
    if st.sidebar.button("PaGe 1"):
        page1()
    if st.sidebar.button("Page 2"):
        page2()
        """
        Note:
        Bug=>
        sometimes when switching pages, line chart dissapeared.
        """
    if st.sidebar.button("Settings"):
        settingsP()