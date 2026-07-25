"""
Email Manager Module for Emma AI
Integrates Gmail and Outlook email checking, filtering, and task creation
"""

import os
import json
import base64
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.api_core.exceptions import GoogleAPIError
    import google.auth
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

try:
    from O365 import Account
    from O365.utils.utils import Folder
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False

import re
from email.utils import parseaddr


class EmailManager:
    """Manages email connections to Gmail and Outlook"""

    def __init__(self, data_dir: str = "data"):
        """Initialize email manager"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Gmail config
        self.gmail_token_path = self.data_dir / "gmail_token.pickle"
        self.gmail_credentials_path = self.data_dir / "gmail_credentials.json"
        self.gmail_service = None

        # Outlook config
        self.outlook_credentials_path = self.data_dir / "outlook_credentials.json"
        self.outlook_account = None

        # Email stats
        self.stats_file = self.data_dir / "email_stats.json"
        self.load_stats()

        # Gmail scopes
        self.GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def load_stats(self):
        """Load email statistics"""
        if self.stats_file.exists():
            with open(self.stats_file, "r", encoding="utf-8") as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                "total_checked": 0,
                "total_created_tasks": 0,
                "last_check": None,
                "email_sources": {"gmail": 0, "outlook": 0},
                "daily_counts": {},
            }

    def save_stats(self):
        """Save email statistics"""
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

    # ============== GMAIL INTEGRATION ==============

    def setup_gmail(self) -> bool:
        """Setup Gmail OAuth connection"""
        if not GMAIL_AVAILABLE:
            return False, "Gmail libraries not installed. Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client"

        try:
            # Check if credentials file exists
            if not self.gmail_credentials_path.exists():
                return (
                    False,
                    f"Gmail credentials.json not found at {self.gmail_credentials_path}. "
                    "Follow: https://developers.google.com/gmail/api/quickstart/python",
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.gmail_credentials_path), self.GMAIL_SCOPES
            )

            # Try to load existing token
            if self.gmail_token_path.exists():
                with open(self.gmail_token_path, "rb") as token_file:
                    creds = pickle.load(token_file)
            else:
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.gmail_token_path, "wb") as token_file:
                pickle.dump(creds, token_file)

            self.gmail_token_path = token_file
            return True, "Gmail connected successfully"

        except Exception as e:
            return False, f"Gmail setup failed: {str(e)}"

    def connect_gmail(self) -> bool:
        """Connect to Gmail API"""
        if not GMAIL_AVAILABLE:
            return False

        try:
            from google.api_core.exceptions import GoogleAPIError
            from googleapiclient.discovery import build

            if self.gmail_token_path.exists():
                with open(self.gmail_token_path, "rb") as token_file:
                    creds = pickle.load(token_file)

                # Refresh token if expired
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())

                self.gmail_service = build("gmail", "v1", credentials=creds)
                return True

        except Exception as e:
            print(f"Gmail connection failed: {e}")
            return False

    def get_gmail_unread_count(self) -> int:
        """Get unread email count from Gmail"""
        if not self.connect_gmail():
            return 0

        try:
            result = self.gmail_service.users().messages().list(
                userId="me", q="is:unread"
            ).execute()
            return result.get("resultSizeEstimate", 0)
        except Exception as e:
            print(f"Error getting Gmail unread count: {e}")
            return 0

    def get_gmail_emails(
        self,
        folder: str = "INBOX",
        unread_only: bool = True,
        limit: int = 10,
        query_filter: str = "",
    ) -> List[Dict]:
        """Fetch emails from Gmail"""
        if not self.connect_gmail():
            return []

        try:
            # Build query
            q = f"is:unread" if unread_only else ""
            if query_filter:
                q += f" {query_filter}"

            # Get message list
            result = (
                self.gmail_service.users()
                .messages()
                .list(userId="me", q=q, maxResults=limit)
                .execute()
            )

            messages = result.get("messages", [])
            emails = []

            for message in messages:
                # Get full message
                msg = (
                    self.gmail_service.users()
                    .messages()
                    .get(userId="me", id=message["id"], format="full")
                    .execute()
                )

                headers = msg["payload"]["headers"]
                email_data = {
                    "id": message["id"],
                    "source": "gmail",
                    "subject": next(
                        (h["value"] for h in headers if h["name"] == "Subject"),
                        "(No Subject)",
                    ),
                    "from": next(
                        (h["value"] for h in headers if h["name"] == "From"),
                        "Unknown",
                    ),
                    "to": next(
                        (h["value"] for h in headers if h["name"] == "To"),
                        "Unknown",
                    ),
                    "date": next(
                        (h["value"] for h in headers if h["name"] == "Date"),
                        datetime.now().isoformat(),
                    ),
                    "snippet": msg.get("snippet", ""),
                    "unread": "UNREAD" in msg.get("labelIds", []),
                }

                # Extract body
                if "parts" in msg["payload"]:
                    for part in msg["payload"]["parts"]:
                        if part["mimeType"] == "text/plain":
                            data = part["body"].get("data", "")
                            if data:
                                email_data["body"] = base64.urlsafe_b64decode(
                                    data
                                ).decode("utf-8")
                            break
                else:
                    data = msg["payload"]["body"].get("data", "")
                    if data:
                        email_data["body"] = base64.urlsafe_b64decode(data).decode(
                            "utf-8"
                        )

                emails.append(email_data)

            self.stats["email_sources"]["gmail"] += len(emails)
            return emails

        except Exception as e:
            print(f"Error getting Gmail emails: {e}")
            return []

    # ============== OUTLOOK INTEGRATION ==============

    def setup_outlook(self, client_id: str, client_secret: str) -> bool:
        """Setup Outlook OAuth connection"""
        if not OUTLOOK_AVAILABLE:
            return False

        try:
            account = Account(
                (client_id, client_secret),
                tenant="common",
                token_backend=None,
            )

            if account.authenticate():
                self.outlook_account = account
                return True
            return False

        except Exception as e:
            print(f"Outlook setup failed: {e}")
            return False

    def get_outlook_unread_count(self) -> int:
        """Get unread email count from Outlook"""
        if not self.outlook_account:
            return 0

        try:
            mailbox = self.outlook_account.mailbox()
            inbox = mailbox.get_folder(folder_name="Inbox")
            unread = inbox.get_messages(
                limit=1, query=mailbox.new_query().on_attribute("isRead").equals(False)
            )
            return len(unread) if unread else 0
        except Exception as e:
            print(f"Error getting Outlook unread count: {e}")
            return 0

    def get_outlook_emails(
        self,
        folder: str = "Inbox",
        unread_only: bool = True,
        limit: int = 10,
        query_filter: str = "",
    ) -> List[Dict]:
        """Fetch emails from Outlook"""
        if not self.outlook_account:
            return []

        try:
            mailbox = self.outlook_account.mailbox()
            folder_obj = mailbox.get_folder(folder_name=folder)

            query = mailbox.new_query()
            if unread_only:
                query = query.on_attribute("isRead").equals(False)

            messages = folder_obj.get_messages(limit=limit, query=query)

            emails = []
            for msg in messages:
                email_data = {
                    "id": msg.object_id,
                    "source": "outlook",
                    "subject": msg.subject or "(No Subject)",
                    "from": msg.sender.name if msg.sender else "Unknown",
                    "to": msg.to_recipients[0].name
                    if msg.to_recipients
                    else "Unknown",
                    "date": msg.received.isoformat()
                    if msg.received
                    else datetime.now().isoformat(),
                    "body": msg.body or "",
                    "snippet": msg.body[:100] if msg.body else "",
                    "unread": not msg.is_read,
                }
                emails.append(email_data)

            self.stats["email_sources"]["outlook"] += len(emails)
            return emails

        except Exception as e:
            print(f"Error getting Outlook emails: {e}")
            return []

    # ============== UNIFIED EMAIL OPERATIONS ==============

    def get_all_unread_count(self) -> Dict[str, int]:
        """Get unread email count from all sources"""
        counts = {"total": 0, "gmail": 0, "outlook": 0}

        if GMAIL_AVAILABLE and self.gmail_credentials_path.exists():
            gmail_count = self.get_gmail_unread_count()
            counts["gmail"] = gmail_count
            counts["total"] += gmail_count

        if OUTLOOK_AVAILABLE and self.outlook_account:
            outlook_count = self.get_outlook_unread_count()
            counts["outlook"] = outlook_count
            counts["total"] += outlook_count

        # Update daily stats
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.stats["daily_counts"]:
            self.stats["daily_counts"][today] = {"emails": 0}
        self.stats["daily_counts"][today]["emails"] = counts["total"]

        self.stats["last_check"] = datetime.now().isoformat()
        self.stats["total_checked"] += 1
        self.save_stats()

        return counts

    def get_important_emails(self, limit: int = 5) -> List[Dict]:
        """Get most important unread emails"""
        all_emails = []

        # Gmail important emails
        if GMAIL_AVAILABLE and self.gmail_credentials_path.exists():
            gmail_emails = self.get_gmail_emails(
                query_filter="is:important OR from:boss OR label:important",
                limit=limit,
            )
            all_emails.extend(gmail_emails)

        # Outlook important emails
        if OUTLOOK_AVAILABLE and self.outlook_account:
            outlook_emails = self.get_outlook_emails(limit=limit)
            all_emails.extend(outlook_emails)

        # Sort by date (most recent first) and limit
        all_emails.sort(key=lambda x: x["date"], reverse=True)
        return all_emails[:limit]

    def get_emails_by_sender(self, sender: str, limit: int = 5) -> List[Dict]:
        """Get emails from specific sender"""
        emails = []

        # Gmail
        if GMAIL_AVAILABLE and self.gmail_credentials_path.exists():
            gmail_emails = self.get_gmail_emails(
                query_filter=f'from:"{sender}"', limit=limit
            )
            emails.extend(gmail_emails)

        # Outlook
        if OUTLOOK_AVAILABLE and self.outlook_account:
            try:
                mailbox = self.outlook_account.mailbox()
                folder = mailbox.get_folder(folder_name="Inbox")
                query = mailbox.new_query().on_attribute("from").contains(sender)
                messages = folder.get_messages(limit=limit, query=query)

                for msg in messages:
                    email_data = {
                        "id": msg.object_id,
                        "source": "outlook",
                        "subject": msg.subject or "(No Subject)",
                        "from": msg.sender.name if msg.sender else "Unknown",
                        "date": msg.received.isoformat()
                        if msg.received
                        else datetime.now().isoformat(),
                        "body": msg.body or "",
                        "snippet": msg.body[:100] if msg.body else "",
                    }
                    emails.append(email_data)
            except Exception as e:
                print(f"Error getting Outlook emails by sender: {e}")

        return emails

    def search_emails(self, keyword: str, limit: int = 5) -> List[Dict]:
        """Search emails by keyword"""
        emails = []

        # Gmail
        if GMAIL_AVAILABLE and self.gmail_credentials_path.exists():
            gmail_emails = self.get_gmail_emails(
                query_filter=f'"{keyword}"', limit=limit
            )
            emails.extend(gmail_emails)

        # Outlook
        if OUTLOOK_AVAILABLE and self.outlook_account:
            try:
                mailbox = self.outlook_account.mailbox()
                folder = mailbox.get_folder(folder_name="Inbox")
                query = (
                    mailbox.new_query()
                    .on_attribute("subject")
                    .contains(keyword)
                    .chain("or")
                    .on_attribute("bodyPreview")
                    .contains(keyword)
                )
                messages = folder.get_messages(limit=limit, query=query)

                for msg in messages:
                    email_data = {
                        "id": msg.object_id,
                        "source": "outlook",
                        "subject": msg.subject or "(No Subject)",
                        "from": msg.sender.name if msg.sender else "Unknown",
                        "date": msg.received.isoformat()
                        if msg.received
                        else datetime.now().isoformat(),
                        "body": msg.body or "",
                        "snippet": msg.body[:100] if msg.body else "",
                    }
                    emails.append(email_data)
            except Exception as e:
                print(f"Error searching Outlook emails: {e}")

        return emails

    def get_email_summary(self) -> str:
        """Get email summary for daily check-in"""
        counts = self.get_all_unread_count()
        total = counts["total"]

        summary = f"📧 **Email Summary**\n"
        summary += f"Total unread: {total}\n"

        if counts["gmail"] > 0:
            summary += f"Gmail: {counts['gmail']} unread\n"
        if counts["outlook"] > 0:
            summary += f"Outlook: {counts['outlook']} unread\n"

        if total > 0:
            important = self.get_important_emails(limit=3)
            if important:
                summary += f"\nTop {len(important)} important emails:\n"
                for email in important:
                    summary += f"  • {email['subject']}\n    From: {email['from']}\n"

        return summary

    def get_stats(self) -> Dict:
        """Get email statistics"""
        return {
            "total_emails_checked": self.stats["total_checked"],
            "total_tasks_created": self.stats["total_created_tasks"],
            "last_check": self.stats["last_check"],
            "sources": self.stats["email_sources"],
            "daily_counts": self.stats["daily_counts"],
        }

    def extract_tasks_from_email(
        self, email: Dict
    ) -> List[Tuple[str, str, str, str]]:
        """Extract potential tasks from email content"""
        tasks = []

        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()
        sender = email.get("from", "")

        # Keywords that suggest tasks
        task_keywords = {
            "action": "high",
            "todo": "high",
            "deadline": "high",
            "urgent": "high",
            "asap": "high",
            "please": "medium",
            "can you": "medium",
            "need your": "medium",
            "follow up": "high",
            "meeting": "medium",
            "review": "medium",
            "send": "medium",
            "confirm": "medium",
        }

        priority = "medium"
        detected_keywords = []

        for keyword, kw_priority in task_keywords.items():
            if keyword in subject or keyword in body[:200]:
                detected_keywords.append(keyword)
                if kw_priority == "high":
                    priority = "high"

        if detected_keywords:
            # Create task title from subject
            task_title = f"Email: {email.get('subject', 'Response needed')[:50]}"

            # Extract deadline if mentioned
            deadline_keywords = [
                "by ",
                "due ",
                "before ",
                "until ",
                "today",
                "tomorrow",
            ]
            deadline = None
            for kw in deadline_keywords:
                if kw in body:
                    # Simple extraction - in production, use NLP
                    deadline = datetime.now().strftime("%Y-%m-%d")
                    break

            tasks.append((task_title, "Messages", priority, sender))

        return tasks

    def create_tasks_from_emails(self, task_manager) -> int:
        """Create tasks from important emails"""
        created = 0
        important_emails = self.get_important_emails(limit=10)

        for email in important_emails:
            tasks = self.extract_tasks_from_email(email)
            for task_title, category, priority, related_to in tasks:
                task_manager.add_task(
                    title=task_title,
                    category=category,
                    priority=priority,
                    notes=f"Related to: {related_to}",
                )
                created += 1

        self.stats["total_created_tasks"] += created
        self.save_stats()
        return created
