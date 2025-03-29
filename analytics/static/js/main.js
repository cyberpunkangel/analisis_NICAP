//Animacion de tecla
let app = document.getElementById('app');

let typewriter = new Typewriter(app, {
    loop: true,
    delay: 50
});

typewriter.typeString('La inteligencia artificial no es una amenaza para la humanidad, sino una oportunidad para mejorarla.')
    .pauseFor(1)
    .deleteAll()
    .start();

//modal
$("#exampleModal").on("shown.bs.modal", function(e) {
    let videoIframe = $("#exampleModal iframe");
    videoIframe.attr("src", "https://mega.nz/embed/sJFB3I5A#7AIR6DRsvY9pbdZe7CLgPLHJATEGdu9yRwPorL_Gip8");
    videoIframe[0].load();
});

$("#exampleModal").on('hidden.bs.modal', function (e) {
    let videoIframe = $("#exampleModal iframe");
    videoIframe.attr("src", "");
});