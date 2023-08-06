import os
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup
from exchangelib import Credentials, Configuration, Account, DELEGATE, FileAttachment

from withpano.app.libraries.constants import SUPPORTED_ATTACHMENT_FILES


class EmailExtractor:
    def __init__(self, server, email, username, password):
        """
        Get Exchange account connection with server
        """
        self.username = username
        self.email = email
        creds = Credentials(username=username, password=password)
        config = Configuration(server=server, credentials=creds)
        self.account = Account(primary_smtp_address=email, autodiscover=False,
                               config=config, access_type=DELEGATE)

    def get_recent_emails(self, folder_name, count):
        """
        Retrieve reverse ranked date received emails for a given folder
        """
        # Get the folder object
        folder = self.account.root / 'Top of Information Store' / folder_name
        # Get emails
        return folder.all().order_by('-datetime_received')[:count]

    def count_senders(self, emails):
        """
        Given emails, provide counts of sender by name
        """
        counts = defaultdict(int)
        for email in emails:
            counts[email.sender.name] += 1
        return counts

    def print_non_replies(self, emails, agents):
        """
        Print subjects where no agents have replied
        """
        dealt_with = dict()
        not_dealt_with = dict()
        not_dealt_with_ordered = list()
        for email in emails:  # newest to oldest
            # Simplify subject
            subject = email.subject.lower().replace('re: ', '')
            if subject in dealt_with or subject in not_dealt_with:
                continue
            elif email.sender.name in agents:
                # If most recent email was from an agent
                dealt_with[subject] = email
            else:
                # Email from anyone else has not been dealt with
                not_dealt_with[subject] = email
                soup = BeautifulSoup(email.body)
                # if email.attachments:
                not_dealt_with_ordered += [
                    {"subject": email.subject, 'sender': f"{email.sender.name}<{email.sender.email_address}>",
                     "body": soup.get_text('\n'), "attachment": [attachment for attachment in email.attachments]}]
        items = []
        for subject in not_dealt_with_ordered:
            items.append(f' * {subject}')
        return items

    def all_emails(self, emails):
        records = []
        for email in emails:  # newest to oldest
            # print(email.sender.name)
            # Simplify subject
            soup = BeautifulSoup(email.body)
            if email.attachments:
                attachment_record = []
                for attachment in email.attachments:
                    if isinstance(attachment, FileAttachment):
                        path = Path(f'./project_data/emails/{email.id}')
                        path.mkdir(parents=True, exist_ok=True)
                        if attachment.content_type in SUPPORTED_ATTACHMENT_FILES:
                            local_path = os.path.join(path, attachment.name)
                            with open(local_path, 'wb') as f:
                                f.write(attachment.content)
                            attachment_record.append({'path': local_path, 'mime_type': attachment.content_type})
                        else:
                            print('Attachment Ignored')
                    # elif isinstance(attachment, ItemAttachment):
                    #     if isinstance(attachment.item, Message):
                    #         print(attachment.item.subject, attachment.item.body)
                records.append(
                    {"id": email.id, "subject": email.subject,
                     'sender': f"{email.sender.name}<{email.sender.email_address}>",
                     "body": soup.get_text('\n'), "attachments": attachment_record})
        return records


"""
    def main():
        # Connection details
        server = 'outlook.office365.com'
        email = 'arun.hazra@hotmail.com'
        username = 'arun.hazra@hotmail.com'
        # password = getpass.getpass()  # prompt for password
        password = "arun@hotmail4321"
        account = connect(server, email, username, password)
        print(account)
        # print_tree(account)
        emails = get_recent_emails(account, "Inbox", 100)
        # counts = count_senders(emails)
        # print(counts)
        agents = {'Vivek': True, 'Divami Design Labs': True}
        # print_non_replies(emails, agents)
        print_non_replies_all(emails)
"""
