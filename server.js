const express = require('express');
const https = require('https');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Route API 
app.get('/api', (req, res) => {
    const sslInfo = {
        ssl_enabled: req.secure,
        ssl_protocol: req.connection.getCipher()?.version || 'N/A',
        ssl_cipher: req.connection.getCipher()?.name || 'N/A',
        server_name: req.hostname,
        timestamp: new Date().toISOString()
    };

    res.json({
        status: 'success',
        message: 'SSL/TLS Server aktif!',
        ssl_info: sslInfo,
        endpoints: {
            'GET /api': 'Get SSL info',
            'POST /api': 'Send data via SSL'
        }
    });
});

app.post('/api', (req, res) => {
    const data = req.body;
    
    const sslInfo = {
        ssl_enabled: req.secure,
        ssl_protocol: req.connection.getCipher()?.version || 'N/A',
        ssl_cipher: req.connection.getCipher()?.name || 'N/A',
        server_name: req.hostname,
        timestamp: new Date().toISOString()
    };

    res.json({
        status: 'success',
        message: 'Data diterima via SSL/TLS',
        received_data: data,
        ssl_info: sslInfo
    });
});

// Static files API routes
app.use(express.static('public'));

// SSL Certificate
const sslOptions = {
    key: fs.readFileSync(path.join(__dirname, 'ssl', 'server.key')),
    cert: fs.readFileSync(path.join(__dirname, 'ssl', 'server.crt'))
};

// Start HTTPS Server
const PORT = 3443;
https.createServer(sslOptions, app).listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('SSL/TLS Server Running');
    console.log('='.repeat(60));
    console.log(`HTTPS Server: https://localhost:${PORT}`);
    console.log(`SSL Certificate: Self-Signed`);
    console.log(`Started at: ${new Date().toLocaleString('id-ID')}`);
    console.log('='.repeat(60));
});

// Optional: HTTP redirect ke HTTPS
const http = require('http');
http.createServer((req, res) => {
    res.writeHead(301, { Location: `https://localhost:${PORT}${req.url}` });
    res.end();
}).listen(3000, () => {
    console.log(`HTTP Redirect: http://localhost:3000 -> https://localhost:${PORT}`);
});
