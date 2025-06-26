const express = require('express');
const path = require('path');
const cors = require('cors');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use('/static', express.static(path.join(__dirname, 'static')));

// Create a placeholder logo if it doesn't exist
const logoDir = path.join(__dirname, 'static', 'images');
const logoPath = path.join(logoDir, 'Logo.png');

if (!fs.existsSync(logoDir)) {
  fs.mkdirSync(logoDir, { recursive: true });
}

// Routes for HTML pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'startseite.html'));
});

app.get('/startseite', (req, res) => {
    res.sendFile(path.join(__dirname, 'startseite.html'));
});

app.get('/uber-tool', (req, res) => {
    res.sendFile(path.join(__dirname, 'uber_tool.html'));
});

app.get('/entwicklerteam', (req, res) => {
    res.sendFile(path.join(__dirname, 'entwicklerteam.html'));
});

app.get('/kontakt', (req, res) => {
    res.sendFile(path.join(__dirname, 'kontakt.html'));
});

app.get('/hilfe', (req, res) => {
    res.sendFile(path.join(__dirname, 'hilfe.html'));
});

app.get('/allg-angaben', (req, res) => {
    res.sendFile(path.join(__dirname, 'allg_angaben.html'));
});

app.get('/baukrper', (req, res) => {
    res.sendFile(path.join(__dirname, 'baukrper.html'));
});

app.get('/baukoerper-kp', (req, res) => {
    res.sendFile(path.join(__dirname, 'baukrper_kp.html'));
});

app.get('/baukrper-kp-2', (req, res) => {
    res.sendFile(path.join(__dirname, 'baukrper_kp_2.html'));
});

app.get('/bauteil', (req, res) => {
    res.sendFile(path.join(__dirname, 'bauteil.html'));
});

app.get('/bauteil-kp', (req, res) => {
    res.sendFile(path.join(__dirname, 'bauteil_kp.html'));
});

app.get('/pv', (req, res) => {
    res.sendFile(path.join(__dirname, 'pv.html'));
});

app.get('/lftung', (req, res) => {
    res.sendFile(path.join(__dirname, 'lftung.html'));
});

app.get('/beleuchtung', (req, res) => {
    res.sendFile(path.join(__dirname, 'beleuchtung.html'));
});

app.get('/beleuchtung-2', (req, res) => {
    res.sendFile(path.join(__dirname, 'beleuchtung_2.html'));
});

app.get('/waermequellen', (req, res) => {
    res.sendFile(path.join(__dirname, 'wrmequellen.html'));
});

app.get('/sdf', (req, res) => {
    res.sendFile(path.join(__dirname, 'sdf.html'));
});

app.get('/gwp', (req, res) => {
    res.sendFile(path.join(__dirname, 'gwp.html'));
});

app.get('/ergebnis', (req, res) => {
    res.sendFile(path.join(__dirname, 'ergebnis.html'));
});

app.get('/einfach-ergebnis', (req, res) => {
    res.sendFile(path.join(__dirname, 'einfach_ergebnis.html'));
});

// API endpoint for energy calculations
app.get('/api/berechnung', (req, res) => {
    // Mock calculation data
    const mockData = {
        nutzenergie: {
            ne_heizung: 35000,
            ne_tww: 10000,
            ne_gesamt: 45000,
            ne_spezifisch: 58.8
        },
        endenergie: {
            ee_heizung: 38000,
            ee_tww: 12000,
            ee_lueftung: 5000,
            ee_beleuchtung: 8000,
            ee_prozesse: 3000,
            ee_gesamt: 66000,
            ee_spezifisch: 86.3
        },
        primaerenergie: {
            pe_gesamt: 78000,
            pe_spezifisch: 102.0
        },
        pv: {
            pv_ertrag: 15000,
            strom_ueberschuss: 5000
        },
        gwp: {
            gwp_var1: 33000,
            gwp_var2: 19800
        },
        gebaeudedaten: {
            hoehe: 8.4,
            grundflaeche: 300,
            volumen: 2520,
            bgf: 900,
            nf: 765
        }
    };
    
    res.json(mockData);
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} to view the application`);
});