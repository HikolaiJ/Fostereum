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
Redderick=pickle.load(open("etc/redderick_model.pkl", "rb"))
a=pd.read_csv("etc/sensor_data (2).csv")

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
            <div id="LogoBut" style="box-shadow:#000000bd 0px 0px 13px 16px;"><img class="centers" style="padding:20px; padding-right:40px; width:100%;" src="data:image/gif;base64,{pr_picLogo}"/></div>
            <p class="centers" style="padding:0;text-shadow:#8e8e8e 7px 5px 10px;color:white;padding-right:35px;width:350px;text-align:center;font-size:57px;font-weight:700;">FOSTEREUM</p>
        </div>
        </div>
    """)
    with open ("etc/scr_home.js") as f:
        html(f"<script>{jz}\n{f.read()}</script>")

#External Contents
def page1():
    plc.html("""
            <div id="CONT" pageState="camerasection">
             <div id="display-cam" class="ection" style="background:#222222;width:765px;height:402px;"></div>
             <div id="content-control" class="ection" style="padding:20px;background:white;width:765px;height:200px;margin-top:20px;box-shadow:inset #00000040 0 0 15px 4px;">
                <div id="container-control">
                    <button><img src="https://i.ibb.co.com/gJg9g4X/Whats-App-Image-2024-07-27-at-3-22-45-PM-removebg-preview.png"></button>
                    <button><img src="https://i.ibb.co.com/S54Wqyd/21981d32-f432-4964-a0c2-c6510e40f243-removebg-preview.png"></button>
                    <button><img style="width:26px; top:4px; left:9px;"src="https://i.ibb.co.com/kQLHNRN/Whats-App-Image-2024-07-27-at-3-22-44-PM-removebg-preview.png"</button>
                </div>
             </div>
            </div>
        """)
    html(f"<script>{jz}</script>")
def page2(): # show prediction and data of sensors
    b=pd.read_csv("etc/25-07-24 Dataset 1.csv")
    a['Timestamp'] = pd.to_datetime(a['Timestamp']).dt.round('15min')
    a['hour'] = a['Timestamp'].dt.hour
    a.dropna(inplace=True)
    yb = Redderick.predict(a[["hour", "Humidity", "Temperature", "Soil Moisture", "MQ135 Value"]])  # Y-axis points
    plc.html(f"""
            <div id="CONT">
             <div class="ection" id="LineGraph-res" style="padding-left:5px; position:relative; background:white; width:753px; height:400px; margin-left:-140px; display:inline-block;">
              <div id="cont-tog" style="position:absolute; bottom:0; padding:16px;">
                <button class="ToggleGr" id="LHum" style=";height:30px;">Humidity</button>
                <button class="ToggleGr" id="LTemp" style="height:30px;">Temperature</button>
                <button class="ToggleGr" id="LMois" style="height:30px;">Soil Moisture</button>
                <button class="ToggleGr" id="LMQ" style="height:30px;">PPM</button>
              </div>
             </div>
             <div class="ection" id="Sensors-det" style="background:#dcffc8; width:250px; height:400px; display:inline-block; margin-left:17px; position:absolute;">
                <div>PPM : {b.iloc[-1]["humidity"]}</div>
                <div>Humidity : {b.iloc[-1]["temperature"]}</div>
                <div>Temperature : {b.iloc[-1]["soilMoisture"]}</div>
                <div>Soil Moisture : {b.iloc[-1]["mq135"]}</div>
             </div>
             
            </div>
        """)
    a["Humidity"]=yb[:,0]
    st.line_chart(a, x='Timestamp', y="Humidity")
    st.line_chart(a, x='Timestamp', y="Temperature")
    st.line_chart(a, x='Timestamp', y="Soil Moisture")
    st.line_chart(a, x='Timestamp', y="MQ135 Value")
    with open ("etc/scr_p2.js") as f:
        html(f"<script>{jz}{f.read()}</script>")
def settingsP():
    plc.html("""
<div id="CONT" style="margin-left:-76px; padding:0px 31px; background:#e7ffe9; height:600px; width:900px; border-radius:13px; box-shadow:inset #00000091 0 0 20px 0px;">
    <h1>Settings</h1>
    <div class="sep" id="Telegram-id">
        <label>Telegram Chat ID</label><input id="telechat-id" placeholder="Enter your telegram chat id..">
    </div>
    <div id="bot-feature">
        <div class="sep"><label>Weekly report</label><div id="week-rep"><label class="switch"><input type="checkbox"><span class="slider round"></span></label></div></div>
        <div class="sep"><label>Alert when plant's environment is not suitable</label><div id="alert-notif"><label class="switch"><input type="checkbox"><span class="slider round"></span></label></div></div>
    </div>
    <div class="sep" id="danger-zone">
        <label style="color:red;">Danger Zone!</label><br>
        <label>Delete all data</label>
             <button id="delete-data" style="margin-left:223px; font-size:10px;background:red;color:white;border-radius:9px;padding:5px;">Delete Data</button>
             <label style="font-style:italic; font-size:9px; margin-left:4px;">*This action will delete all data from your local storage.</label>
    </div>
</div>
    """)
    with open ("etc/scr_setting.js") as f:
        html(f"<script>{jz}\n{f.read()}</script>")


#Start web
if __name__ == "__main__":
    with open ("etc/style.css", "r") as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
    main()
    if st.sidebar.button("Home"):
        main()
    if st.sidebar.button("Monitor"):
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