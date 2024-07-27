(async function() {
    await waitFor(()=>parent.document.getElementById("CONT"));
    parent.document.getElementById("CONT").setAttribute("pageState", "setting");
    await waitFor(() => parent.document.getElementById("telechat-id"));
    parent.document.getElementById("telechat-id").addEventListener("blur", (e) => {
        var a={};
        if (localStorage.getItem("Fostereum-Session")) {
            a=JSON.parse(localStorage.getItem("Fostereum-Session"));
        }
        if (e.target.value.length == 0) {
            let el = document.createElement("div");
            el.textContent = "Please enter your telechat ID, you can get it from ";
            let el2 = document.createElement("a");
            el2.href = "https://t.me/FostereumBot";
            el2.textContent = "https://t.me/FostereumBot";
            el.appendChild(el2);
            el.setAttribute("style", "color: red;font-style: italic;position: absolute;right: 180px;font-size: 10px;padding-top: 5px;");
            parent.document.getElementById("telechat-id").parentNode.appendChild(el);
        }
        a.teleid=e.target.value;
        localStorage.setItem("Fostereum-Session", JSON.stringify(a));
        console.log(a);
    });
    parent.document.getElementById("delete-data").addEventListener("click", () => {
        localStorage.removeItem("Fostereum-Session");
        console.log("%cUser data has been deleted.", "color: red; font-style: italic;");
    });
    parent.document.getElementById("alert-notif").addEventListener("click", (event) => {
        event.target.getElementsByTagName("input")[0].classList.toggle("checked");
        var a = localStorage.getItem("Fostereum-Session")? JSON.parse(localStorage.getItem("Fostereum-Session")) : {};
        if (event.target.getElementsByTagName("input")[0].classList.contains("checked")) {
            a.alertnotif = true;
        } else {
            a.alertnotif = false;
        }
    });
    parent.document.getElementById("week-rep").addEventListener("click", (event) => {
        event.target.getElementsByTagName("input")[0].classList.toggle("checked");
        var a = localStorage.getItem("Fostereum-Session")? JSON.parse(localStorage.getItem("Fostereum-Session")) : {};
        if (event.target.getElementsByTagName("input")[0].classList.contains("checked")) {
            a.weekreport = true;
        } else {
            a.weekreport = false;
        }
    });
    
    var assignedData = localStorage.getItem("Fostereum-Session");
    if (assignedData) {
        var data = JSON.parse(assignedData);
        parent.document.getElementById("telechat-id").value = data.teleid;
        if (data.alertnotif) {
            parent.document.getElementById("alert-notif").getElementsByTagName("input")[0].classList.add("checked");
        }
        if (data.weekreport) {
            parent.document.getElementById("week-rep").getElementsByTagName("input")[0].classList.add("checked");
        }
    }
})();