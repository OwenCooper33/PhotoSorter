const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

const db = new sqlite3.Database("emails.db", (err) => {
    if (err) console.error(err.message);
    console.log("Connected to SQLite database.");
});

db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE)");

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/submit", (req, res) => {
    const email = req.body.email;

    if (!email) {
        return res.send("Please enter a valid email.");
    }

    db.run("INSERT INTO users (email) VALUES (?)", [email], (err) => {
        if (err) {
            console.error(err.message);
            return res.send("Error saving email. Maybe it's already registered.");
        }
        console.log(`Email saved: ${email}`);

        res.send(`
            <h2>Thank you!</h2>
            <p>Your email has been recorded.</p>
            <a href="/download">Download the Program</a>
        `);
    });
});

app.get("/download", (req, res) => {
    const filePath = path.join(__dirname, "dist", "photo_sorter");
    res.download(filePath, "photo_sorter", (err) => {
        if (err) console.error(err);
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
