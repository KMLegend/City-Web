const om_emps = [
    "AZURE COMPACT LIFE",
    "HAUT COMPACT LIFE BY CITY",
    "INFINITY BUSINESS",
    "BLANC CASA DESIGN",
    "EPIC CITY HOME",
    "TERRAÇO BOUGAINVILLE",
    "ATMOS CITY DESIGN",
    "LEGACY CITY HOME",
    "CITY RICARDO PARANHOS",
  ];

  var imagemLogo = document.createElement("img");
  imagemLogo.src =
    "https://city-solucoes.com/static/imagens/logo_black.png";
  imagemLogo.style.alignSelf = "flex-end";

  let flagFirstRender = false;

  let dropdown = document.getElementById("emps");
  if (dropdown) {
    dropdown.addEventListener("change", () => {
        setTimeout(() => {
        let divPrincipal = document.querySelector(
            "#emp_display > div.flex.justify-center.align-middle"
        );

        updateLogo();

        if (!flagFirstRender) {
            divPrincipal.appendChild(imagemLogo);

            flagFirstRender = true;
        }
        }, 500);
    });
}
  function updateLogo() {
    if (om_emps.includes(dropdown.value)) {
      imagemLogo.style.maxWidth = "20vw";
      imagemLogo.style.maxHeight = "100vh";
      imagemLogo.src = "https://city-solucoes.com/static/imagens/CITY_OM_LOGO_BLACK.png";
    } else {
      imagemLogo.style.maxWidth = "15vw";
      imagemLogo.src =
        "https://city-solucoes.com/static/imagens/logo_black.png";
    }
  }