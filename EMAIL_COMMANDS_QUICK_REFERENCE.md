# 📧 Emma AI - Email Commands Quick Reference

## PC Terminal Commands

### Check Emails
```bash
check emails
```
Shows:
- Unread count (Gmail + Outlook)
- Top 5 important emails
- Sender and subject

### Get Email Summary
```bash
email summary
```
Shows formatted summary ready for daily check-in

### Search Emails
```bash
search emails <keyword>
```

**Examples:**
```bash
search emails work              # Find emails about "work"
search emails project deadline  # Multi-word search
search emails invoice           # Search for invoices
```

### Find Emails from Specific Person
```bash
emails from <sender>
```

**Examples:**
```bash
emails from boss                # All emails from boss
emails from john@company.com    # Specific email address
emails from client              # All emails from "client"
```

### View Email Statistics
```bash
email stats
```

Shows:
- Total emails checked
- Tasks created from emails
- Last check time
- Gmail vs Outlook split
- Daily email counts

---

## 📱 Phone API Calls

### Base URL
```
http://<your-pc-ip>:5000
```

**How to find your PC IP:**

Windows:
```
ipconfig
# Look for "IPv4 Address" like 192.168.1.100
```

### API Endpoints

#### Get Unread Count
```
GET /api/emails/unread
```

**Example:**
```bash
curl http://192.168.1.100:5000/api/emails/unread
```

**Response:**
```json
{
  "total": 5,
  "gmail": 3,
  "outlook": 2,
  "timestamp": "2026-07-25T08:50:00"
}
```

#### Get Important Emails
```
GET /api/emails/important?limit=5
```

**Example:**
```bash
curl http://192.168.1.100:5000/api/emails/important?limit=10
```

**Response:**
```json
{
  "emails": [
    {
      "id": "msg123",
      "source": "gmail",
      "subject": "Project deadline",
      "from": "boss@company.com",
      "date": "2026-07-25T08:30:00",
      "snippet": "Please complete the project by Friday..."
    }
  ],
  "count": 1,
  "timestamp": "2026-07-25T08:50:00"
}
```

#### Search Emails
```
GET /api/emails/search?q=<keyword>&limit=10
```

**Examples:**
```bash
curl http://192.168.1.100:5000/api/emails/search?q=work
curl http://192.168.1.100:5000/api/emails/search?q=meeting&limit=5
```

**Response:**
```json
{
  "emails": [...],
  "count": 3,
  "keyword": "work",
  "timestamp": "2026-07-25T08:50:00"
}
```

#### Get Emails from Sender
```
GET /api/emails/from/<sender>?limit=10
```

**Examples:**
```bash
curl http://192.168.1.100:5000/api/emails/from/boss
curl http://192.168.1.100:5000/api/emails/from/john@company.com?limit=5
```

**Response:**
```json
{
  "emails": [...],
  "count": 5,
  "sender": "boss",
  "timestamp": "2026-07-25T08:50:00"
}
```

#### Get Email Statistics
```
GET /api/emails/stats
```

**Example:**
```bash
curl http://192.168.1.100:5000/api/emails/stats
```

**Response:**
```json
{
  "stats": {
    "total_emails_checked": 42,
    "total_tasks_created": 8,
    "last_check": "2026-07-25T08:45:00",
    "sources": {
      "gmail": 120,
      "outlook": 45
    },
    "daily_counts": {
      "2026-07-25": {"emails": 5}
    }
  },
  "timestamp": "2026-07-25T08:50:00"
}
```

---

## 🔌 JavaScript Fetch Examples

### React/React Native

```javascript
// Check unread emails
const checkEmails = async () => {
  try {
    const response = await fetch('http://192.168.1.100:5000/api/emails/unread');
    const data = await response.json();
    console.log(`${data.total} unread emails`);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Get important emails
const getImportantEmails = async () => {
  try {
    const response = await fetch('http://192.168.1.100:5000/api/emails/important?limit=10');
    const data = await response.json();
    data.emails.forEach(email => {
      console.log(`${email.subject} - from ${email.from}`);
    });
  } catch (error) {
    console.error('Error:', error);
  }
};

// Search emails
const searchEmails = async (keyword) => {
  try {
    const response = await fetch(
      `http://192.168.1.100:5000/api/emails/search?q=${keyword}&limit=10`
    );
    const data = await response.json();
    console.log(`Found ${data.count} emails for "${keyword}"`);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Get emails from sender
const getEmailsFromSender = async (sender) => {
  try {
    const response = await fetch(
      `http://192.168.1.100:5000/api/emails/from/${sender}?limit=10`
    );
    const data = await response.json();
    console.log(`Found ${data.count} emails from ${sender}`);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Get stats
const getEmailStats = async () => {
  try {
    const response = await fetch('http://192.168.1.100:5000/api/emails/stats');
    const data = await response.json();
    console.log(`Total checked: ${data.stats.total_emails_checked}`);
    console.log(`Last check: ${data.stats.last_check}`);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 📊 Email Data Format

Each email object contains:

```json
{
  "id": "unique_message_id",
  "source": "gmail",  // or "outlook"
  "subject": "Email subject line",
  "from": "sender@email.com",
  "to": "you@email.com",
  "date": "2026-07-25T08:30:00",
  "body": "Full email body text",
  "snippet": "First 100 characters of email...",
  "unread": true
}
```

---

## 🎯 Common Tasks

### Check All Unread Emails
```bash
check emails
```

### Find Emails from Your Boss
```bash
emails from boss
```

### Search for Important Emails
```bash
search emails urgent
```

### Get Statistics
```bash
email stats
```

### Setup for Mobile App
1. Run API server: `python api_server.py`
2. Get your PC IP: `ipconfig`
3. In app, use: `http://<ip>:5000/api/emails/unread`

---

## ⚙️ Setup Required

### Install Libraries
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client O365
```

### Configure Gmail
1. Download credentials from Google Cloud Console
2. Save as `data/gmail_credentials.json`
3. Run `check emails` (will open browser for auth)

### Configure Outlook
1. Create Azure app for your account
2. Save credentials as `data/outlook_credentials.json`:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

---

## 🚨 Troubleshooting

| Problem | Fix |
|---------|-----|
| **"Email integration not available"** | Run `pip install -r requirements.txt` |
| **Gmail auth fails** | Delete `data/gmail_token.pickle` and retry |
| **"Credentials not found"** | Save `gmail_credentials.json` to `data/` |
| **"Permission denied"** | Check Google Account Security settings |
| **Phone can't connect** | Verify PC IP and firewall allows port 5000 |
| **No emails found** | Check if unread emails exist in inbox |

---

## 📈 Performance Tips

- First check takes ~2-3 seconds (loading libraries)
- Subsequent checks are faster
- Limit results with `?limit=5` to speed up searches
- Run API server once, leave it running for phone

---

## 🔐 Security Notes

- OAuth tokens stored locally at `data/gmail_token.pickle`
- Never commit credentials to git
- Email data never sent to external servers
- Full privacy - all processing local

---

**Ready to use?**

```bash
# Start Emma
python main.py

# Then type
check emails
```

Happy emailing! 📧🚀
