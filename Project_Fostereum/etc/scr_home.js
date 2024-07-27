(async function(){
    if (!localStorage.getItem("Fostereum-Session")) {
        localStorage.setItem("Fostereum-Session", "{}");
        console.log("%cWelcome new user to Fostereum!", "font-weight:bold; color:#00ff00; font-size:20px;");
        a=document.createElement("div");
        a.setAttribute("id", "popup-f");
        a.setAttribute("style", "width:800px; height:545px; padding-left:46px;");
        a.innerHTML=`<h1 style="text-align:center;">Welcome to Fostereum!</h1>
    <p style="text-align:center;">Fostereum is an automated care and maintenance for indoor plants<br>that are accessible whenever.</p>
    <h3>This website provide the following feature:</h3>
    <p>
        <ul style="display:inline-block;">
            <li>Monitor your plant's health</li>
            <li>Automated care and maintenance</li>
            <li>Monitor your plant's water and air quality</li>
            <li>Connect to your home Wi-Fi</li>
            <li>Monitor your plant's humidity and temperature</li>
            <li>Monitor your plant's soil moisture</li>
            <li>Monitor your plant's MQ135 value</li>
            <li>Weekly report of your plant's condition</li>
            <li>Alert when plant's environment is not compatible</li>
        </ul>
        <img style="height:auto;width:118px;position:absolute;bottom:25%;right:19%;" src="https://i.ibb.co.com/7KZBvDM/29010270-removebg-preview.png"></img>
    </p>
    </p>`
        await waitFor(() => parent.document.getElementById("CONT"));
        parent.document.getElementById("CONT").appendChild(a);
        a.addEventListener("blur", () => {
            a.remove();
        });
    }
})();