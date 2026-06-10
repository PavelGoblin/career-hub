const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve website static files
app.use(express.static(path.join(__dirname, 'website')));

// Serve markdown files from book directory
app.use('/book', express.static(path.join(__dirname)));

// Fallback to index.html
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'website', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`\n📘 Cybersecurity Book Server`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`🚀 Server: http://localhost:${PORT}`);
    console.log(`📖 Open browser → http://localhost:${PORT}`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━\n`);
});
