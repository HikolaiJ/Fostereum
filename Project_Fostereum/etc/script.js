window.addEventListener('resize', (e)=> {
    p2_graph = parent.document.getElementsByTagName("canvas")[0].parentElement.parentElement.parentElement.parentElement
    if (parent.document.getElementById("LineGraph-res") && !p2_graph.classList.contains("inserted-OE")) {
        p2_graph.classList.add("inserted-OE");
        console.log("resize and added class");
    }
});