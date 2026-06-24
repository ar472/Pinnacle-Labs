// ==========================
// LIVE CLOCK
// ==========================

function updateClock() {

    const clock =
        document.getElementById(
            "live-clock"
        );

    if (!clock) return;

    const now = new Date();

    clock.innerHTML =
        now.toLocaleTimeString();
}

setInterval(
    updateClock,
    1000
);

updateClock();


// ==========================
// DARK MODE
// ==========================

function toggleTheme() {

    document.body.classList.toggle(
        "dark-mode"
    );

    const theme =
        document.body.classList.contains(
            "dark-mode"
        )
        ? "dark"
        : "light";

    localStorage.setItem(
        "theme",
        theme
    );

    const btn =
        document.getElementById(
            "theme-btn"
        );

    if(btn){

        btn.innerHTML =
        theme === "dark"
        ? "☀️ Light Mode"
        : "🌙 Dark Mode";
    }
}

window.addEventListener(
    "load",
    () => {

        const savedTheme =
            localStorage.getItem(
                "theme"
            );

        if(savedTheme === "dark"){

            document.body.classList.add(
                "dark-mode"
            );

            const btn =
                document.getElementById(
                    "theme-btn"
                );

            if(btn){

                btn.innerHTML =
                    "☀️ Light Mode";
            }
        }
    }
);


// ==========================
// VOICE SEARCH
// ==========================

function startVoiceSearch(){

    if(
        !(
            "webkitSpeechRecognition"
            in window
        )
    ){

        alert(
            "Voice Search Not Supported"
        );

        return;
    }

    const recognition =
        new webkitSpeechRecognition();

    recognition.lang = "en-IN";

    recognition.start();

    recognition.onresult =
    function(event){

        const city =
            event.results[0][0]
            .transcript;

        document.getElementById(
            "cityInput"
        ).value = city;

        document.querySelector(
            "form"
        ).submit();
    };
}
// ==========================
// SEARCH HISTORY
// ==========================

function saveHistory(city){

    let history =
        JSON.parse(
            localStorage.getItem(
                "weatherHistory"
            )
        ) || [];

    history = history.filter(
        item => item !== city
    );

    history.unshift(city);

    history = history.slice(0,8);

    localStorage.setItem(
        "weatherHistory",
        JSON.stringify(history)
    );

    showHistory();
}

function showHistory(){

    const list =
        document.getElementById(
            "history-list"
        );

    if(!list) return;

    list.innerHTML = "";

    const history =
        JSON.parse(
            localStorage.getItem(
                "weatherHistory"
            )
        ) || [];

    history.forEach(city => {

        const li =
            document.createElement("li");

        li.innerHTML =
            "📍 " + city;

        li.style.cursor =
            "pointer";

        li.onclick = () => {

            document.getElementById(
                "cityInput"
            ).value = city;

            document.querySelector(
                "form"
            ).submit();
        };

        list.appendChild(li);
    });
}


// ==========================
// SAVE CURRENT CITY
// ==========================

window.addEventListener(
    "load",
    () => {

        showHistory();

        const cityHeading =
            document.querySelector(
                ".weather-card h2"
            );

        if(cityHeading){

            saveHistory(
                cityHeading.innerText
            );
        }
    }
);


// ==========================
// QUICK SEARCH
// ==========================

function quickSearch(city){

    document.getElementById(
        "cityInput"
    ).value = city;

    document.querySelector(
        "form"
    ).submit();
}


// ==========================
// FAVORITE CITIES STORAGE
// ==========================

function addFavorite(city){

    let favorites =
        JSON.parse(
            localStorage.getItem(
                "favorites"
            )
        ) || [];

    if(
        !favorites.includes(city)
    ){

        favorites.push(city);
    }

    localStorage.setItem(
        "favorites",
        JSON.stringify(favorites)
    );
}


// ==========================
// WEATHER ALERT POPUP
// ==========================

window.addEventListener(
    "load",
    () => {

        const alerts =
            document.querySelectorAll(
                ".alert-item"
            );

        if(
            alerts.length > 0
        ){

            setTimeout(() => {

                alert(
                    "⚠ Weather Alert Available"
                );

            },1000);
        }
    }
);
// ==========================
// GEOLOCATION
// ==========================

function getLocation(){

    if(
        !navigator.geolocation
    ){

        alert(
            "Geolocation Not Supported"
        );

        return;
    }

    navigator.geolocation
    .getCurrentPosition(

        function(position){

            const lat =
                position.coords.latitude;

            const lon =
                position.coords.longitude;

            alert(
                "📍 Location Detected\n\nLatitude: "
                + lat +
                "\nLongitude: "
                + lon
            );
        },

        function(){

            alert(
                "Location Access Denied"
            );
        }
    );
}


// ==========================
// AQI ANIMATION
// ==========================

window.addEventListener(
    "load",
    () => {

        const aqiCircle =
            document.querySelector(
                ".aqi-circle"
            );

        if(aqiCircle){

            aqiCircle.animate(

                [

                    {
                        transform:
                        "scale(.8)"
                    },

                    {
                        transform:
                        "scale(1)"
                    }

                ],

                {

                    duration:1200,

                    iterations:1
                }
            );
        }
    }
);


// ==========================
// TEMPERATURE CHART
// ==========================

window.addEventListener(
    "load",
    () => {

        const chartCanvas =
            document.getElementById(
                "tempChart"
            );

        if(
            chartCanvas &&
            typeof forecastTemps !==
            "undefined"
        ){

            new Chart(

                chartCanvas,

                {

                    type:"line",

                    data:{

                        labels:
                        forecastDates,

                        datasets:[

                            {

                                label:
                                "Temperature °C",

                                data:
                                forecastTemps,

                                borderWidth:
                                3,

                                tension:
                                0.4,

                                fill:false
                            }
                        ]
                    },

                    options:{

                        responsive:true,

                        maintainAspectRatio:false,

                        plugins:{

                            legend:{

                                labels:{

                                    color:
                                    "white"
                                }
                            }
                        },

                        scales:{

                            x:{

                                ticks:{

                                    color:
                                    "white"
                                }
                            },

                            y:{

                                ticks:{

                                    color:
                                    "white"
                                }
                            }
                        }
                    }
                }
            );
        }
    }
);


// ==========================
// LEAFLET MAP
// ==========================

window.addEventListener(
    "load",
    () => {

        if(
            typeof latitude !==
            "undefined"
        ){

            const map =
                L.map("map")
                .setView(

                    [
                        latitude,
                        longitude
                    ],

                    10
                );

            L.tileLayer(

                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

                {

                    attribution:
                    "© OpenStreetMap"
                }

            ).addTo(map);

            L.marker(

                [
                    latitude,
                    longitude
                ]

            ).addTo(map)

            .bindPopup(
                "📍 Weather Location"
            )

            .openPopup();
        }
    }
);


// ==========================
// CARD ANIMATIONS
// ==========================

document.addEventListener(

    "DOMContentLoaded",

    () => {

        const cards =

        document.querySelectorAll(

            ".forecast-card, \
             .hour-card, \
             .rain-card, \
             .weather-card, \
             .aqi-card"
        );

        cards.forEach(

            (card,index)=>{

                card.style.opacity =
                    "0";

                card.style.transform =
                    "translateY(20px)";

                setTimeout(()=>{

                    card.style.transition =
                        "0.6s ease";

                    card.style.opacity =
                        "1";

                    card.style.transform =
                        "translateY(0)";

                },index*100);
            }
        );
    }
);
// ==========================
// PWA INSTALL BUTTON
// ==========================

let deferredPrompt;

window.addEventListener(
    "beforeinstallprompt",
    (e) => {

        e.preventDefault();

        deferredPrompt = e;

        const installBtn =
            document.getElementById(
                "installBtn"
            );

        if (installBtn) {

            installBtn.style.display =
                "inline-block";
        }
    }
);

const installBtn =
document.getElementById(
    "installBtn"
);

if (installBtn) {

    installBtn.addEventListener(
        "click",

        async () => {

            if (!deferredPrompt)
                return;

            deferredPrompt.prompt();

            await deferredPrompt.userChoice;

            deferredPrompt = null;
        }
    );
}


// ==========================
// FAVORITE CITY AUTO SAVE
// ==========================

window.addEventListener(
    "load",
    () => {

        const cityHeading =

        document.querySelector(
            ".weather-card h2"
        );

        if (cityHeading) {

            addFavorite(
                cityHeading.innerText
            );
        }
    }
);


// ==========================
// RADAR ANIMATION
// ==========================

window.addEventListener(
    "load",
    () => {

        const radar =

        document.querySelector(
            ".radar-placeholder"
        );

        if (radar) {

            radar.animate(

                [
                    { opacity: 0.5 },
                    { opacity: 1 },
                    { opacity: 0.5 }
                ],

                {
                    duration: 2500,
                    iterations: Infinity
                }
            );
        }
    }
);


// ==========================
// SMOOTH SCROLL
// ==========================

document.documentElement.style.scrollBehavior =
"smooth";


// ==========================
// BUTTON HOVER EFFECTS
// ==========================

document.querySelectorAll(
    "button"
).forEach(

    btn => {

        btn.addEventListener(
            "mouseenter",

            () => {

                btn.style.transition =
                    ".3s";

                btn.style.transform =
                    "translateY(-3px)";
            }
        );

        btn.addEventListener(
            "mouseleave",

            () => {

                btn.style.transform =
                    "translateY(0)";
            }
        );
    }
);


// ==========================
// PAGE FADE EFFECT
// ==========================

window.addEventListener(
    "load",

    () => {

        document.body.style.opacity =
            "0";

        setTimeout(() => {

            document.body.style.transition =
                "opacity .8s";

            document.body.style.opacity =
                "1";

        }, 100);
    }
);