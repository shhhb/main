from datetime import date
import pandas as pd
from send_email import send_email


SHEET_ID = "1iVI5x-nUsYl8ZMp7rFv4HZ5pe2Jn9RbUjMxHmWMPWwA"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"



def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df




def query_data_and_send_emails(df):
    present_date = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if row['has_paid'] == 'no' and present_date in (row['reminder_date'].date(), row['due_date'].date()):
            send_email(
                subject=f"[Payment Reminder] Invoice: {row['invoice_number']}",
                reciever_email=row['email'],
                name=row['name'],
                due_date=row['due_date'].strftime("%d, %b %Y"),
                invoice_no=row['invoice_number'],
                amount=row['amount']
            )
            email_counter += 1
    return f"Total emails sent: {email_counter}"


df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)
        
