const API_BASE = "";

const apiStatus = document.getElementById("apiStatus");
const discoveryForm = document.getElementById("discoveryForm");
const analysisResult = document.getElementById("analysisResult");
const exploreButton = document.getElementById("exploreButton");


// Afficher un message
function showMessage(message) {
    analysisResult.textContent = message;
}


// Vérifier le serveur
async function checkServer() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);

        if (!response.ok) {
            throw new Error("Serveur indisponible");
        }

        const data = await response.json();

        apiStatus.textContent =
            data.status === "online" ? "EN LIGNE" : "INDISPONIBLE";

    } catch (error) {
        apiStatus.textContent = "EN ATTENTE";
        console.error("Erreur serveur :", error);
    }
}


// Charger les modules depuis le serveur
async function loadModules() {
    try {
        const response = await fetch(`${API_BASE}/api/modules`);

        if (!response.ok) {
            throw new Error("Impossible de charger les modules");
        }

        const data = await response.json();

        console.log("Modules JOSNEXUS AI :", data.modules);

    } catch (error) {
        console.error("Erreur modules :", error);
    }
}


// Envoyer une demande d'analyse
discoveryForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = document
        .getElementById("question")
        .value.trim();

    const domain = document
        .getElementById("domain")
        .value;

    if (question.length < 3) {
        showMessage("Veuillez écrire une question plus précise.");
        return;
    }

    const submitButton = discoveryForm.querySelector(
        'button[type="submit"]'
    );

    submitButton.disabled = true;
    submitButton.textContent = "ANALYSE EN COURS...";

    showMessage("JOSNEXUS AI reçoit votre demande...");

    try {
        const response = await fetch(`${API_BASE}/api/discovery`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                domain: domain
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail
                    ? JSON.stringify(data.detail)
                    : "Erreur pendant la demande"
            );
        }

        showMessage(
            `${data.analysis}\n\n` +
            `Domaine : ${data.domain}\n` +
            `Statut : ${data.status}\n` +
            `Sources connectées : ${data.sources.length}`
        );

    } catch (error) {
        showMessage(
            "Impossible de contacter le serveur. " +
            "Vérifiez votre connexion et réessayez."
        );

        console.error("Erreur analyse :", error);

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "ENVOYER LA DEMANDE →";
    }
});


// Bouton explorer
exploreButton.addEventListener("click", () => {
    document.getElementById("discovery").scrollIntoView({
        behavior: "smooth"
    });
});


// Initialisation
document.addEventListener("DOMContentLoaded", () => {
    checkServer();
    loadModules();
});


// Mise à jour de l'état du serveur
setInterval(checkServer, 30000);


// Service Worker pour la PWA
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/static/sw.js")
            .catch(error => {
                console.error("Service Worker :", error);
            });
    });
        }
