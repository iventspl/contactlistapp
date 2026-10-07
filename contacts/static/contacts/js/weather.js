// Loads current weather for every cell marked with data-weather-city.
// Each unique city is requested only once, and requests are sent one after another
// to avoid bursts of calls to the external APIs (the server caches the results).
const weatherTable = document.querySelector('[data-weather-url]');

if (weatherTable) {
    loadWeather(weatherTable.dataset.weatherUrl);
}

async function loadWeather(weatherUrl) {
    const cells = [...document.querySelectorAll('[data-weather-city]')];
    const cities = new Set(cells.map((cell) => cell.dataset.weatherCity));

    // for-of because it will cause ban from Nominatim if forEach was used
    for (const city of cities) {
        const text = await fetchWeatherText(weatherUrl, city);
        cells
            .filter((cell) => cell.dataset.weatherCity === city)
            .forEach((cell) => { cell.textContent = text; });
    }
}

async function fetchWeatherText(weatherUrl, city) {
    try {
        const response = await fetch(`${weatherUrl}?${new URLSearchParams({ city })}`);
        if (response.status === 404) return 'Unknown city';
        if (!response.ok) return 'Unavailable';

        const weather = await response.json();
        return `${weather.temperature} °C · ${weather.humidity}% · ${weather.wind_speed} km/h`;
    } catch {
        return 'Unavailable';
    }
}
