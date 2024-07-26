function waitFor(conditionFunction) {
    const poll = resolve => {
        if(conditionFunction()) resolve();
        else setTimeout(_ => poll(resolve), 400);
    }
  return new Promise(poll);
}

  
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


window.addEventListener('online', () => console.log('Became online'));
window.addEventListener('offline', () => notconnected());
if (!window.navigator.onLine) {
    notconnected();
}*/
(async function(){
    await waitFor(() => parent.document.getElementById("COK"));
    await waitFor(()=> parent.document.getElementsByTagName("canvas")[0].parentElement.parentElement.parentElement.parentElement);
    await parent.document.getElementById("COK").appendChild(parent.document.getElementsByTagName("canvas")[0].parentElement.parentElement.parentElement.parentElement);
    parent.document.getElementsByTagName("canvas")[0].parentElement.parentElement.parentElement.parentElement.classList.add("inserted-OE");
})();