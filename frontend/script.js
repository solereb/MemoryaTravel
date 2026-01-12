const API_BASE_URL = `http://${window.location.hostname}:8000`;

const iso3to2 = {
    "AFG": "AF", "ALB": "AL", "DZA": "DZ", "ASM": "AS", "AND": "AD",
    "AGO": "AO", "AIA": "AI", "ATA": "AQ", "ATG": "AG", "ARG": "AR",
    "ARM": "AM", "ABW": "AW", "AUS": "AU", "AUT": "AT", "AZE": "AZ",
    "BHS": "BS", "BHR": "BH", "BGD": "BD", "BRB": "BB", "BLR": "BY",
    "BEL": "BE", "BLZ": "BZ", "BEN": "BJ", "BMU": "BM", "BTN": "BT",
    "BOL": "BO", "BIH": "BA", "BWA": "BW", "BVT": "BV", "BRA": "BR",
    "IOT": "IO", "BRN": "BN", "BGR": "BG", "BFA": "BF", "BDI": "BI",
    "KHM": "KH", "CMR": "CM", "CAN": "CA", "CPV": "CV", "CYM": "KY",
    "CAF": "CF", "TCD": "TD", "CHL": "CL", "CHN": "CN", "CXR": "CX",
    "CCK": "CC", "COL": "CO", "COM": "KM", "COG": "CG", "COD": "CD",
    "COK": "CK", "CRI": "CR", "CIV": "CI", "HRV": "HR", "CUB": "CU",
    "CYP": "CY", "CZE": "CZ", "DNK": "DK", "DJI": "DJ", "DMA": "DM",
    "DOM": "DO", "ECU": "EC", "EGY": "EG", "SLV": "SV", "GNQ": "GQ",
    "ERI": "ER", "EST": "EE", "ETH": "ET", "FLK": "FK", "FRO": "FO",
    "FJI": "FJ", "FIN": "FI", "FRA": "FR", "GUF": "GF", "PYF": "PF",
    "ATF": "TF", "GAB": "GA", "GMB": "GM", "GEO": "GE", "DEU": "DE",
    "GHA": "GH", "GIB": "GI", "GRC": "GR", "GRL": "GL", "GRD": "GD",
    "GLP": "GP", "GUM": "GU", "GTM": "GT", "GIN": "GN", "GNB": "GW",
    "GUY": "GY", "HTI": "HT", "HMD": "HM", "VAT": "VA", "HND": "HN",
    "HKG": "HK", "HUN": "HU", "ISL": "IS", "IND": "IN", "IDN": "ID",
    "IRN": "IR", "IRQ": "IQ", "IRL": "IE", "ISR": "IL", "ITA": "IT",
    "JAM": "JM", "JPN": "JP", "JOR": "JO", "KAZ": "KZ", "KEN": "KE",
    "KIR": "KI", "PRK": "KP", "KOR": "KR", "KWT": "KW", "KGZ": "KG",
    "LAO": "LA", "LVA": "LV", "LBN": "LB", "LSO": "LS", "LBR": "LR",
    "LBY": "LY", "LIE": "LI", "LTU": "LT", "LUX": "LU", "MAC": "MO",
    "MKD": "MK", "MDG": "MG", "MWI": "MW", "MYS": "MY", "MDV": "MV",
    "MLI": "ML", "MLT": "MT", "MHL": "MH", "MTQ": "MQ", "MRT": "MR",
    "MUS": "MU", "MYT": "YT", "MEX": "MX", "FSM": "FM", "MDA": "MD",
    "MCO": "MC", "MNG": "MN", "MNE": "ME", "MSR": "MS", "MAR": "MA",
    "MOZ": "MZ", "MMR": "MM", "NAM": "NA", "NRU": "NR", "NPL": "NP",
    "NLD": "NL", "ANT": "AN", "NCL": "NC", "NZL": "NZ", "NIC": "NI",
    "NER": "NE", "NGA": "NG", "NIU": "NU", "NFK": "NF", "MNP": "MP",
    "NOR": "NO", "OMN": "OM", "PAK": "PK", "PLW": "PW", "PSE": "PS",
    "PAN": "PA", "PNG": "PG", "PRY": "PY", "PER": "PE", "PHL": "PH",
    "PCN": "PN", "POL": "PL", "PRT": "PT", "PRI": "PR", "QAT": "QA",
    "REU": "RE", "ROU": "RO", "RUS": "RU", "RWA": "RW", "SHN": "SH",
    "KNA": "KN", "LCA": "LC", "SPM": "PM", "VCT": "VC", "WSM": "WS",
    "SMR": "SM", "STP": "ST", "SAU": "SA", "SEN": "SN", "SRB": "RS",
    "SYC": "SC", "SLE": "SL", "SGP": "SG", "SVK": "SK", "SVN": "SI",
    "SLB": "SB", "SOM": "SO", "ZAF": "ZA", "SGS": "GS", "ESP": "ES",
    "LKA": "LK", "SDN": "SD", "SUR": "SR", "SJM": "SJ", "SWZ": "SZ",
    "SWE": "SE", "CHE": "CH", "SYR": "SY", "TWN": "TW", "TJK": "TJ",
    "TZA": "TZ", "THA": "TH", "TLS": "TL", "TGO": "TG", "TKL": "TK",
    "TON": "TO", "TTO": "TT", "TUN": "TN", "TUR": "TR", "TKM": "TM",
    "TCA": "TC", "TUV": "TV", "UGA": "UG", "UKR": "UA", "ARE": "AE",
    "GBR": "GB", "USA": "US", "UMI": "UM", "URY": "UY", "UZB": "UZ",
    "VUT": "VU", "VEN": "VE", "VNM": "VN", "VGB": "VG", "VIR": "VI",
    "WLF": "WF", "ESH": "EH", "YEM": "YE", "ZMB": "ZM", "ZWE": "ZW"
};

let map;
let geoJsonLayer;
let countryMapping = {};
let selectedCountryId = null;
let selectedCountryName = null;
let selectedRegionId = null;
let CACHED_PROFILE = null;

function getCookie(name) {
    const value = `; ${document.cookie};`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function deleteAllCookies() {
        const allCookies = document.cookie.split(';');
        for (let i = 0; i < allCookies.length; i++) {
            const cookie = allCookies[i];
            const eqPos = cookie.indexOf('=');
            const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
            
            document.cookie = name.trim() + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/';
        }
    }

async function Reset() {
    const refresh = getCookie('rememberToken');
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'refresh_token': refresh }),
        credentials: 'include'
    });
    if (response.ok) {
        const data = await response.json();
        deleteAllCookies();
        document.cookie = `rememberToken=${data.refresh_token}; path=/; max-age=604800`;
        return true;
    }
    deleteAllCookies();
    window.location.href = '/login.html';
    return false;
}

document.addEventListener('DOMContentLoaded', async () => {
    initProfile();
    await initMap();
});

const descInput = document.getElementById('travelDescription');
const charCounter = document.getElementById('charCounter');

descInput.addEventListener('input', () => {
    const length = descInput.value.length;
    charCounter.textContent = `${length} / 5000`;
    
    if (length > 4500) {
        charCounter.style.color = 'red';
    } else {
        charCounter.style.color = '#bbb';
    };
});

async function initProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/profile`, { credentials: 'include' });
        if (response.ok) {
            const profile = await response.json();
            const img = document.getElementById('userAvatar');
            img.src = `${API_BASE_URL}/users/avatar?t=${Date.now()}`;
            CACHED_PROFILE = profile
        } else if (response.status === 401) {
            await Reset();
            initProfile();
        }
    } catch (e) { console.error("Ошибка профиля", e); }
}

async function initMap() {
    map = L.map('map-container').setView([20, 0], 2);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap & CartoDB',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    try {
        const response = await fetch(`${API_BASE_URL}/geography/countries`, { credentials: 'include' });
        const countriesData = await response.json();
        countriesData.forEach(c => {
            countryMapping[c.code] = c; 
        });
        const select = document.getElementById('countrySelectModal');
        countriesData.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = c.name_ru;
            select.appendChild(opt);
        });

    } catch (e) {
        console.error("Не удалось загрузить страны с бэкенда", e);
    }
    const geoResponse = await fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json');
    const geoData = await geoResponse.json();
    geoJsonLayer = L.geoJson(geoData, {
        style: styleFeature,
        onEachFeature: onEachFeature
    }).addTo(map);
    await checkUrlParams();
}
function styleFeature(feature) {
    return {
        fillColor: '#8FBFC0',
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.5
    };
}
let is_locked = false;
function onEachFeature(feature, layer) {
    const code3 = feature.id;
    const code2 = iso3to2[code3];

    if (!code2) return;
    const backendData = countryMapping[code2];
    if (backendData) {
        layer.backendId = backendData.id;
        layer.countryName = backendData.name_ru;
    }

    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: clickCountry
    });
}
function highlightFeature(e) {
    if (is_locked === true) return;
    const layer = e.target;
    layer.setStyle({
        weight: 2,
        color: '#666',
        fillOpacity: 0.8
    });
}

function resetHighlight(e) {
    if (is_locked === true) return;
    geoJsonLayer.resetStyle(e.target);
}
const CIS_COUNTRIES = ["RU"]; 
let regionsLayer = null;

function normalizeName(text) {
    if (!text) return "";

    let clean = text.toLowerCase();
    const stopWords = [
        "область", "обл\\.", "обл",      
        "город", "г\\.", "г",            
        "район", "р-н",                  
        "поселок", "посёлок", "пос\\.", "пос",
        "село", "с\\.", "с",             
        "деревня", "д\\.", "д",          
        "улица", "ул\\.", "ул",          
        "пгт",                           
        "микрорайон", "мкр",              
        "республика", 'респ\\.', 'респ'
    ];
    const pattern = new RegExp(`(^|\\s)(${stopWords.join('|')})(?=[\\s.,]|$)`, 'gi');
    
    clean = clean.replace(pattern, '');

    // 3. Финальная зачистка
    clean = clean.replace(/[.,()]/g, ' ');
    clean = clean.replace(/\s+/g, ' ');    
    
    return clean.trim(); 
}
const CUSTOM_VIEWS = {
    "RU": { center: [64.0, 95.0], zoom: 3 }, 
};
async function clickCountry(e) {
    const layer = e.target;
    const feature = layer.feature;
    const code3 = feature.id;
    const code2 = iso3to2[code3];

    if (!layer.backendId) {
        alert("Эта страна пока не добавлена в базу данных");
        return;
    }

    selectedCountryId = layer.backendId;
    selectedCountryName = layer.countryName;
    updateSidebarUI(selectedCountryName);
    if (code2 && CIS_COUNTRIES.includes(code2)) {
        await enterRegionMode(code2, selectedCountryId, layer);
    } else {
        loadTravelsForCountry(selectedCountryId, selectedCountryName);
    }
}
function toggleMapInteraction(isActive) {
    if (isActive) {
        map.dragging.enable();
        map.touchZoom.enable();
        map.doubleClickZoom.enable();
        map.scrollWheelZoom.enable();
        map.boxZoom.enable();
        map.keyboard.enable();
        if (map.tap) map.tap.enable();
        document.getElementById('map-container').style.cursor = 'grab';
    } else {
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
        map.boxZoom.disable();
        map.keyboard.disable();
        if (map.tap) map.tap.disable();
        document.getElementById('map-container').style.cursor = 'default';
    }
}

async function enterRegionMode(iso2Code, countryId, layer) {
    geoJsonLayer.eachLayer(function (l) {
        l.setStyle({
            fillColor: '#f0f0f0', 
            color: '#ddd',
            weight: 1,
            fillOpacity: 0.3
        });
    });
    toggleMapInteraction(false);
    is_locked = true;
    if (CUSTOM_VIEWS[iso2Code]) {
        const view = CUSTOM_VIEWS[iso2Code];
        map.setView(view.center, view.zoom, { animate: true });
    } else {
        map.fitBounds(layer.getBounds(), { padding: [50, 50], animate: true });
    }
    if (regionsLayer) {
        map.removeLayer(regionsLayer);
    }
    let backendRegions = [];
    try {
        const response = await fetch(`${API_BASE_URL}/geography/regions/${countryId}`, { credentials: 'include' });
        backendRegions = await response.json();
    } catch (e) { console.error(e); }
    try {
        const geoResponse = await fetch(`/static/${iso2Code}.geojson`);
        if (!geoResponse.ok) throw new Error();
        const geoData = await geoResponse.json();
        
        regionsLayer = L.geoJson(geoData, {
            style: styleRegion,
            onEachFeature: (feature, l) => onEachRegion(feature, l, backendRegions)
        }).addTo(map);
        
        regionsLayer.bringToFront();
        loadTravelsForCountry(countryId, selectedCountryName);
    } catch (e) {
        
        loadTravelsForCountry(countryId, selectedCountryName);
    }
}

function styleRegion(feature) {
    return {
        fillColor: '#FFD700',
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.4
    };
}

function onEachRegion(feature, layer, backendRegions) {
    const regionNameGeo = feature.properties.name || feature.properties.name_ru || feature.properties.NAME_1 || feature.properties.region;
    
    const matchedRegion = backendRegions.find(r => 
        normalizeName(r.name_ru) === normalizeName(regionNameGeo)
    );

    if (matchedRegion) {
        layer.regionId = matchedRegion.id;
        layer.bindTooltip(matchedRegion.name_ru);
    }

    layer.on({
        mouseover: (e) => {
            e.target.setStyle({ weight: 2, fillOpacity: 0.7 });
        },
        mouseout: (e) => {
            regionsLayer.resetStyle(e.target);
        },
        click: (e) => {
            L.DomEvent.stopPropagation(e);
            if (matchedRegion) {
                updateSidebarUI(`${regionNameGeo}`)
                loadTravelsRegion(matchedRegion.id, regionNameGeo)
                selectedRegionId = matchedRegion.id;
            } else {
                
            }
        }
    });
}
let selectedFiles = [];

const mediaInput = document.getElementById('mediaInput');
const mediaPreviewGrid = document.getElementById('mediaPreviewGrid');
const mediaCounter = document.getElementById('mediaCounter');
const mediaAddBtn = document.getElementById('mediaAddBtn');

mediaInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    if (selectedFiles.length + files.length === 5) {
        document.getElementById('mediaAddBtn').style.display = 'none';
    }

    files.forEach(file => {
        selectedFiles.push(file);
        renderPreview(file);
    });
});

function renderPreview(file) {
    const reader = new FileReader();
    const item = document.createElement('div');
    item.className = 'media-item';

    reader.onload = (e) => {
        if (file.type.startsWith('image/')) {
            item.innerHTML = `<img src="${e.target.result}">`;
        } else if (file.type.startsWith('video/')) {
            item.innerHTML = `<video src="${e.target.result}"></video>`;
        }
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-media';
        removeBtn.innerHTML = '&times;';
        removeBtn.onclick = () => {
            selectedFiles = selectedFiles.filter(f => f !== file);
            item.remove();
            document.getElementById('mediaAddBtn').style.display = 'flex';
        };
        item.appendChild(removeBtn);
    };

    reader.readAsDataURL(file);
    mediaPreviewGrid.appendChild(item);
}

async function loadTravelsRegion(regionId, selectedRegionName) {
    const contentDiv = document.getElementById('sidebarContent');
    contentDiv.innerHTML = '<p>Загрузка...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/travels/by_region/${regionId}`, {
            credentials: 'include'
        });
        
        const travels = await response.json();
        
        if (travels.length === 0) {
            contentDiv.innerHTML = `
                <div class="info-message">
                    Нет путешествий в регионе <b>${selectedRegionName}.<br>
                    Нажмите <b>+</b>, чтобы добавить!
                </div>
            `;
            contentDiv.innerHTML += `<div id=selectedCountryDisplay></div>`
            contentDiv.innerHTML += `<button class="btn-select" onclick="resetSelection()">Сбросить выбор</button>`
        } else {
            let html = `<h3>Путешествия:</h3>`;
            
            travels.forEach(t => {
            const iconsHtml = t.icon_ids && t.icon_ids.length > 0 
                ? t.icon_ids.map(id => `<img src="static/${id}.png" class="travel-card-icon">`).join('')
                : '';

            html += `
                <div class="travel-item">
                    <div class="travel-card-main" onclick="openViewModal('${t.id}')" style="cursor: pointer;">
                        <h4 class="travel-title">${t.title}</h4>
                        <small class="travel-date">${t.travel_date}</small>
                        <div class="travel-card-icons">
                            ${iconsHtml}
                        </div>
                    </div>
                </div>`;
        });
            contentDiv.innerHTML = html;
            contentDiv.innerHTML += `<div id=selectedCountryDisplay></div>`
            contentDiv.innerHTML += `<button class="btn-select" onclick="resetSelection()">Сбросить выбор</button>`
        }

    } catch (e) {
        contentDiv.innerHTML = '<p>Ошибка загрузки данных</p>';
        console.error(e);
    }
}

async function loadTravelsForCountry(countryId, selectedCountryName) {
    const contentDiv = document.getElementById('sidebarContent');
    contentDiv.innerHTML = '<p>Загрузка...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/travels/by_country/${countryId}`, {
            credentials: 'include'
        });
        
        const travels = await response.json();
        
        if (travels.length === 0) {
            contentDiv.innerHTML = `
                <div class="info-message">
                    Нет путешествий в стране <b>${selectedCountryName}</b>.<br>
                    Нажмите <b>+</b>, чтобы добавить!
                </div>
            `;
            contentDiv.innerHTML += `<div id=selectedCountryDisplay></div>`
            contentDiv.innerHTML += `<button class="btn-select" onclick="resetSelection()">Сбросить выбор</button>`
        } else {
            let html = `<h3>Путешествия:</h3>`;
            
            travels.forEach(t => {
            const iconsHtml = t.icon_ids && t.icon_ids.length > 0 
                ? t.icon_ids.map(id => `<img src="static/${id}.png" class="travel-card-icon">`).join('')
                : '';

            html += `
                <div class="travel-item">
                    <div class="travel-card-main" onclick="openViewModal('${t.id}')" style="cursor: pointer;">
                        <h4 class="travel-title">${t.title}</h4>
                        <small class="travel-date">${t.travel_date}</small>
                        <div class="travel-card-icons">
                            ${iconsHtml}
                        </div>
                    </div>
                </div>`;
        });
            contentDiv.innerHTML = html;
            contentDiv.innerHTML += `<div id=selectedCountryDisplay></div>`
            contentDiv.innerHTML += `<button class="btn-select" onclick="resetSelection()">Сбросить выбор</button>`
        }

    } catch (e) {
        contentDiv.innerHTML = '<p>Ошибка загрузки данных</p>';
        console.error(e);
    }
}

function updateSidebarUI(name) {
    document.getElementById('sidebarTitle').textContent = name;1
    document.getElementById('selectedCountryDisplay').style.color = "white";
}

async function resetSelection() {
    selectedCountryId = null;
    selectedCountryName = null;
    selectedRegionId = null;
    if (regionsLayer) {
        map.removeLayer(regionsLayer);
        regionsLayer = null;
    }

    toggleMapInteraction(true);

    document.getElementById('sidebarTitle').textContent = "Добавить путешествие";
    document.getElementById('sidebarContent').innerHTML = `
        <div class="info-message">
            <p>Нажимайте на страны, чтобы увидеть свои путешествия.</p>
        </div>
        <div class="country-hint" id="selectedCountryDisplay">Выберите страну на карте</div>
        <button class="btn-select" onclick="resetSelection()">Сбросить выбор</button>
    `;
    if (is_locked === true){
        const geoResponse = await fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json');
        const geoData = await geoResponse.json();
        geoJsonLayer = L.geoJson(geoData, {
            style: styleFeature,
            onEachFeature: onEachFeature
        }).addTo(map);
        is_locked = false
    };
    map.setView([20, 0], 2);
}

async function openViewModal(travelId) {
    try {
        const response = await fetch(`${API_BASE_URL}/travels/by_id/${travelId}`, { credentials: 'include' });
        if (response.status === 401){
            Reset();
            openViewModal(travelId);
        };
        const travel = await response.json();
        
        document.getElementById('viewTitle').textContent = travel.title;
        document.getElementById('viewDate').textContent = new Date(travel.travel_date).toLocaleDateString('ru-RU');
        document.getElementById('viewLocation').textContent = `${travel.country_name}, ${travel.region_name}`;
        document.getElementById('viewDescription').textContent = travel.description;

        if (travel.icon_ids){
            const iconsBox = document.getElementById('viewIcons');
            iconsBox.innerHTML = travel.icon_ids.map(id => 
                `<img src="static/${id}.png" class="travel-card-icon" style="width:50px; height:50px;">`
            ).join('');
        }
        const slider = document.getElementById('mediaSlider');
        const dotsContainer = document.getElementById('sliderDots');
        slider.innerHTML = '';
        dotsContainer.innerHTML = '';
        p = [1,2,3,4]
        if (travel.media && travel.media.length >= 1) {
            travel.media.forEach((item, index) => {
                const mediaHtml =  `<img src="${API_BASE_URL}/travels/image/${travelId}/${item}" alt="">`;
                slider.insertAdjacentHTML('beforeend', mediaHtml);

                const dot = document.createElement('div');
                dot.className = `dot ${index === 0 ? 'active' : ''}`;
                dot.onclick = () => {
                    slider.scrollTo({ left: slider.offsetWidth * index, behavior: 'smooth' });
                };
                dotsContainer.appendChild(dot);
            });
            slider.onscroll = () => {
                const scrollIndex = Math.round(slider.scrollLeft / slider.offsetWidth);
                const dots = dotsContainer.querySelectorAll('.dot');
                dots.forEach((d, i) => d.classList.toggle('active', i === scrollIndex));
            };
        }
        const footerActions = document.querySelector('.view-actions');
        footerActions.innerHTML = `
            <button class="btn-delete" onclick="handleDelete('${travel.id}', '${travel.country_id}')">Удалить</button>
        `;

        document.getElementById('viewModal').style.display = 'flex';
    } catch (e) {
        console.error("Ошибка при открытии карточки:", e);
    }
}

function closeViewModal() {
    document.getElementById('viewModal').style.display = 'none';
}

async function handleDelete(travelId, countryId) {
    const confirmed = confirm("Вы уверены, что хотите удалить это путешествие? Это действие нельзя отменить.")
    if (!confirmed) return;
    try{
        const response = await fetch(`${API_BASE_URL}/travels/by_id/${travelId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        if (response.ok){
            alert('Путешествие удалено')
            closeViewModal();

            loadTravelsForCountry(countryId)
        } else if (response.status === 401){
            await Reset();
            const response = await fetch(`${API_BASE_URL}/travels/by_id/${travelId}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (response.ok){
                alert('ПУтешествие удалено')
                closeViewModal();

                loadTravelsForCountry(countryId)
            } else if (response.status === 401){
                window.location.href = '/login.html'
            }
        }
    } catch (e) {
        
        alert('Не удалось удалить')
    }
}

const cleanErrors = () => {
                const allErrorElements = document.querySelectorAll('.error-message')
                allErrorElements.forEach(err => {
                    err.classList.add('hidden');
                })
            }
        
const displayError = (message) => {
        const allErrorElements = document.querySelectorAll('.error-message')
        allErrorElements.forEach(err => {
            err.textContent = message;
            err.classList.remove('hidden');
        })
    }

let selectedIcons = new Set();

document.querySelectorAll('.icon-item').forEach(item => {
    item.addEventListener('click', () => {
        const iconId = parseInt(item.dataset.id);
        
        if (selectedIcons.has(iconId)) {
            selectedIcons.delete(iconId);
            item.classList.remove('active');
        } else {
            if (selectedIcons.size < 5) {
                selectedIcons.add(iconId);
                item.classList.add('active');
            };
        }
    });
});

async function loadRegions(countryId) {
    const regionSelect = document.getElementById('regionSelectModal');
    regionSelect.innerHTML = '<option value="">Загрузка...</option>';
    
    if (!countryId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/geography/regions/${countryId}`, { credentials: 'include' });
        const regions = await response.json();
        
        regionSelect.innerHTML = '<option value="">Выберите регион...</option>';
        regions.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r.id;
            opt.textContent = r.name_ru;
            regionSelect.appendChild(opt);
        });
        if (selectedRegionId) {
            regionSelect.value = selectedRegionId;
        }
    } catch (e) {
        regionSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
    }
}

function closeAddModal() {
    const modal = document.getElementById('addModal');
    modal.style.display = 'none';
}

function openAddModal() {
    
    const modal = document.getElementById('addModal');
    const countrySelect = document.getElementById('countrySelectModal');
    modal.style.display = 'flex';
    selectedIcons.clear();
    document.querySelectorAll('.icon-item').forEach(i => i.classList.remove('active'));
    if (countrySelect.options.length <= 1) {
        Object.values(countryMapping).forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = c.name_ru;
            countrySelect.appendChild(opt);
        });
    }
    if (selectedCountryId) {
        countrySelect.value = selectedCountryId;
        loadRegions(selectedCountryId);
    }
}
document.getElementById('addTravelForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const payload = {
        title: document.getElementById('travelTitle').value,
        date: document.getElementById('travelDate').value,
        country_id: parseInt(document.getElementById('countrySelectModal').value),
        region_id: parseInt(document.getElementById('regionSelectModal').value),
        description: document.getElementById('travelDescription').value || null,
        icon_ids: Array.from(selectedIcons) 
    };
    if (Object.is(payload.country_id, NaN)){
        displayError('Вы не выбрали страну')
        return;
    }; 
    if (Object.is(payload.region_id, NaN)){
        displayError('Вы не выбрали регион')
        return;
    }
    if (payload.title.length < 5 || payload.title.length > 20) {
        displayError('Длина названия от 5 до 20 символов')
        return;
    };

    
    response = await fetch (`${API_BASE_URL}/travels/create`, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json'},
            credentials: 'include'
    });
    try{
        if (response.ok){
            const data = await response.json();
            const travelId = data.id;
            if (travelId && selectedFiles.length > 0) {
                const formData = new FormData();
                
                selectedFiles.forEach(file => {
                    formData.append('files', file);
                });

                await fetch(`${API_BASE_URL}/travels/${travelId}/upload-media`, {
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                });
            }
            cleanErrors();
            loadTravelsForCountry(parseInt(document.getElementById('countrySelectModal').value), document.getElementById('countrySelectModal').textContent);
            closeAddModal();
        } else if (response.status === 401){
            await Reset();
            response = await fetch (`${API_BASE_URL}/travels/create`, {
                method: 'POST',
                body: JSON.stringify(payload),
                headers: { 'Content-Type': 'application/json'},
                credentials: 'include'
            });
            if (response.ok){
                cleanErrors();
                loadTravelsForCountry(parseInt(document.getElementById('countrySelectModal').value), document.getElementById('countrySelectModal').textContent);
                closeAddModal();
            } else {
                window.location.href = '/401.html';
            }
        }
    } catch (e){
        
        window.location.href = '/500.html'
    }
    
});

async function checkUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const travelId = urlParams.get('id');
    const countryId = urlParams.get('countryId');
    const countryName = urlParams.get('countryName');
    
    
    if (travelId && countryId) {
        
        await updateSidebarUI(countryName);
        await loadTravelsForCountry(parseInt(countryId), countryName);
        openViewModal(travelId);
    }
};