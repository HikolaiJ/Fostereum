/*function notconnected() {
    if (document.getElementById("CONT")) {
    document.getElementById("CONT").innerHTML = `<h1>There's no internet.</h1>
<p>Please connect to the internet to ensure the website runs successfully</p><br>
<p>Then reload the page.<p>`
    } else {
    document.body.innerHTML = `<h1>There's no internet.</h1>
<p>Please connect to the internet to ensure the website runs successfully</p><br>
<p>Then reload the page.<p>`
    }
}
*/
var lE = []
function ToggleGraph(id) {
    for (let i = 0; i < lE.length; i++) {
        if (!lE[i].classList.contains("hd")) {
            lE[i].classList.add("hd");
        }
    }
    parent.document.getElementById(id).classList.remove("hd");
}

/*
window.addEventListener('online', () => console.log('Became online'));
window.addEventListener('offline', () => notconnected());
if (!window.navigator.onLine) {
    notconnected();
}*/

(async function(){
    var col = ["Humidity", "Temperature", "Soil Moisture", "MQ135 Value"]
    await waitFor(()=>parent.document.getElementById("CONT"));
    parent.document.getElementById("CONT").setAttribute("pageState", "graphic-sensors");
    await waitFor(() => parent.document.getElementById("LineGraph-res"));
    await waitFor(()=> parent.document.getElementsByClassName("marks").length == 4);
    for (let i = 0; i < parent.document.getElementsByClassName("marks").length; i++) {
        a=parent.document.getElementsByClassName("marks")[i].parentElement.parentElement.parentElement.parentElement
        parent.document.getElementById("LineGraph-res").insertBefore(a, parent.document.getElementById("cont-tog"));
        a.classList.add("inserted-OE");
        a.classList.add("hd");
        a.setAttribute("id", col[i]);
        lE.push(a);
    }
    lE[0].classList.remove("hd");
    var cil = ["LHum", "LTemp", "LMois", "LMQ"]
    for (let i = 0; i < col.length; i++) {
        parent.document.getElementById(cil[i]).addEventListener("click", () => ToggleGraph(col[i]));
    }
})();