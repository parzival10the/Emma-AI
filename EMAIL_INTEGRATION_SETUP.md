# 📧 Emma AI - Email Integration Setup Guide

Emma can now check your emails from **Gmail** and **Outlook** on both your **PC and phone**!

## ✨ What Emma Can Do With Your Emails

- ✅ **Check unread emails** - Know how many emails are waiting
- ✅ **Get important emails** - See your most urgent messages
- ✅ **Search emails** - Find specific emails by keyword
- ✅ **Filter by sender** - Get emails from specific people
- ✅ **Email statistics** - Track email volume and trends
- ✅ **Create tasks from emails** - Automatically convert important emails into tasks

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Email Libraries

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client O365
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Email Service

#### Option A: Gmail Setup (2 minutes)

**Part 1: Create Google API Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (name: "Emma AI")
3. Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Click "Create Credentials"
   - Choose "OAuth 2.0 Client ID"
   - Select "Desktop application"
   - Download the JSON file

**Part 2: Add Credentials to Emma**

1. Save the JSON file as `data/gmail_credentials.json`
2. Run Emma and type `check emails`
3. A browser window will open - click "Allow"
4. Done! Emma now has access to your Gmail

#### Option B: Outlook Setup (2 minutes)

**Part 1: Create Azure App**

1. Go to [Azure Portal](https://portal.azure.com)
2. Select "Azure Active Directory" → "App registrations"
3. Click "New registration"
4. Name: "Emma AI"
5. Redirect URI: `http://localhost:8000`
6. Create a client secret
7. Copy Client ID and Client Secret

**Part 2: Add Credentials to Emma**

1. Create `data/outlook_credentials.json`:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

2. Run Emma and type `check emails`
3. Done! Emma now has access to your Outlook

### Step 3: Start Using Email Commands

```bash
python main.py
```

Then use commands:

```
check emails        # See unread count and important emails
email summary       # Get summary of all emails
search emails work  # Search for emails about "work"
emails from boss    # See emails from specific sender
email stats         # View email statistics
```

---

## 📱 Using Email on Phone

### Prerequisites

- API server running on PC: `python api_server.py`
- Both phone and PC on same WiFi

### API Endpoints Available

**Check unread count:**
```
GET http://<pc-ip>:5000/api/emails/unread
```

**Get important emails:**
```
GET http://<pc-ip>:5000/api/emails/important?limit=5
```

**Search emails:**
```
GET http://<pc-ip>:5000/api/emails/search?q=keyword
```

**Get emails from sender:**
```
GET http://<pc-ip>:5000/api/emails/from/<sender>
```

**Get email stats:**
```
GET http://<pc-ip>:5000/api/emails/stats
```

### React Native Mobile App Integration

Update your mobile app to use email endpoints:

```javascript
// App.js - Add Email tab

import axios from 'axios';

const EmailTab = () => {
  const [unreadCount, setUnreadCount] = useState(0);
  const [importantEmails, setImportantEmails] = useState([]);

  const checkEmails = async () => {
    try {
      const response = await axios.get(`http://${API_IP}:5000/api/emails/unread`);
      setUnreadCount(response.data.total);
    } catch (error) {
      console.error('Error checking emails:', error);
    }
  };

  const getImportantEmails = async () => {
    try {
      const response = await axios.get(`http://${API_IP}:5000/api/emails/important?limit=10`);
      setImportantEmails(response.data.emails);
    } catch (error) {
      console.error('Error getting emails:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📧 Emails</Text>
      <Text style={styles.unread}>Unread: {unreadCount}</Text>
      
      <ScrollView>
        {importantEmails.map((email, index) => (
          <View key={index} style={styles.emailItem}>
            <Text style={styles.subject}>{email.subject}</Text>
            <Text style={styles.from}>{email.from}</Text>
          </View>
        ))}
      </ScrollView>
      
      <Button title="Refresh" onPress={() => {
        checkEmails();
        getImportantEmails();
      }} />
    </View>
  );
};
```

---

## 🔐 Security Best Practices

### Gmail OAuth

- ✅ Never share your `gmail_credentials.json` file
- ✅ Emma never stores your password
- ✅ OAuth tokens are refreshed automatically
- ✅ Tokens stored locally at `data/gmail_token.pickle`

### Outlook

- ✅ Never commit `outlook_credentials.json` to git
- ✅ Use environment variables for production:

```bash
# Set environment variables
export OUTLOOK_CLIENT_ID="your_client_id"
export OUTLOOK_CLIENT_SECRET="your_client_secret"
```

### Data Privacy

- ✅ All email data stays on your devices
- ✅ Emma reads only email metadata (subject, sender, date)
- ✅ Full email body is retrieved only when needed
- ✅ No data sent to external servers

---

## 📝 Email Commands Reference

### PC Commands

| Command | What it does |
|---------|-------------|
| `check emails` | Show unread count and top 5 important emails |
| `email summary` | Get formatted email summary |
| `search emails <keyword>` | Search all emails for keyword |
| `emails from <sender>` | Show emails from specific person |
| `email stats` | View email statistics |

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/emails/unread` | GET | Get unread email counts |
| `/api/emails/summary` | GET | Get email summary |
| `/api/emails/important` | GET | Get important emails |
| `/api/emails/search` | GET | Search emails |
| `/api/emails/from/<sender>` | GET | Get emails from sender |
| `/api/emails/stats` | GET | Get email statistics |

### Query Parameters

```bash
# Limit results
?limit=10

# Search keyword
?q=keyword

# Combine
?q=work&limit=5
```

---

## 🛠️ Troubleshooting

### "Email integration not available"

**Fix:**
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client O365
```

### Gmail: "Credentials not found"

**Fix:**
1. Download credentials from Google Cloud Console
2. Save as `data/gmail_credentials.json`
3. Run `check emails` again

### Gmail: "Permission denied"

**Fix:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "Less secure app access" (or use 2FA + App password)
3. Delete `data/gmail_token.pickle`
4. Run `check emails` to re-authenticate

### Outlook: "Authentication failed"

**Fix:**
1. Verify Client ID and Secret in `data/outlook_credentials.json`
2. Check Azure app permissions (Mail.Read scope)
3. Ensure redirect URI matches (http://localhost:8000)

### "No emails found"

**Fix:**
1. Check if unread emails exist in your inbox
2. For important emails, ensure they have:
   - "Important" label (Gmail)
   - Or flagged status (Outlook)
3. Verify email address in credentials has emails

### Phone: "Cannot connect to API"

**Fix:**
1. Ensure API server running: `python api_server.py`
2. Check firewall allows port 5000
3. Use correct PC IP address
4. Both devices on same WiFi network

---

## 🔄 Automatic Email Integration

### In Daily Check-in

Emma will automatically include email summary:

```
Emma: Good morning, Parzival! 🌅

📧 Email Summary
Total unread: 5
Gmail: 3 unread
Outlook: 2 unread

Top 3 important emails:
  • Project deadline update
    From: boss@company.com
  • Client meeting confirmed
    From: client@email.com
  • Team sync at 3 PM
    From: team-lead@company.com

You have 8 pending tasks today...
```

### Auto-Create Tasks from Emails

Future feature: Emma can automatically create tasks from important emails.

Enable in settings:

```json
{
  "email_settings": {
    "auto_create_tasks": true,
    "task_keywords": ["action", "todo", "deadline", "urgent"],
    "task_priority": "high"
  }
}
```

---

## 📊 Email Statistics

Emma tracks:

- **Total emails checked** - How many times you checked
- **Tasks created** - How many tasks from emails
- **Daily counts** - Emails per day
- **Email sources** - Gmail vs Outlook split

View with: `email stats`

---

## 🎯 Advanced Usage

### Search by Multiple Criteria

Gmail queries:
```
search emails is:unread from:boss  # Gmail syntax
search emails has:attachment       # Emails with attachments
search emails is:important         # Important emails
```

### Email Filtering

```python
# In your custom setup
from skills.email_manager import EmailManager

manager = EmailManager()

# Get unread emails from last 24 hours
emails = manager.get_gmail_emails(
    query_filter='newer_than:1d',
    unread_only=True
)
```

### Integrate with Task Manager

```python
# Auto-convert important emails to tasks
from skills.email_manager import EmailManager
from skills.task_manager import TaskManager

email_manager = EmailManager()
task_manager = TaskManager()

# Create tasks from emails
created = email_manager.create_tasks_from_emails(task_manager)
print(f"Created {created} tasks from emails")
```

---

## 📱 Mobile App Email Screen

Expected mobile app email interface:

```
┌─────────────────────────────────┐
│ 📧 Emails                       │
├─────────────────────────────────┤
│ Total Unread: 5                 │
│ Gmail: 3 | Outlook: 2           │
│                                 │
│ 🔝 Important:                   │
│ ├─ Project deadline (boss)      │
│ ├─ Meeting confirmed (client)   │
│ └─ Team sync (lead)             │
│                                 │
│ Search: ___________  [Search]   │
│                                 │
│ Recent Emails:                  │
│ ├─ [From: boss@...              │
│ │  Budget review needed]        │
│ ├─ [From: team@...              │
│ │  Code review ready]           │
│ └─ [From: client@...            │
│    Feedback on design]          │
│                                 │
│ [Refresh]      [Compose]        │
└─────────────────────────────────┘
```

---

## 🚀 Next Steps

1. ✅ Install email libraries
2. ✅ Set up Gmail or Outlook
3. ✅ Test commands on PC
4. ✅ Start using `check emails`
5. ✅ Set up mobile app endpoints
6. ✅ View emails on phone too

---

## 📞 Support

**For Gmail issues:**
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Cloud Console](https://console.cloud.google.com)

**For Outlook issues:**
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/api/overview)
- [Azure Portal](https://portal.azure.com)

**For Emma AI issues:**
- Check `data/emma.log` for error details
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Verify internet connection and email access

---

## 🎉 You're Ready!

Emma can now:
- 📧 Check your emails
- 🔍 Search them
- 📊 Show statistics
- 📱 Sync to your phone
- 🤖 Create tasks from emails

**Start using:** `python main.py` → `check emails`

Happy emailing! 🚀
