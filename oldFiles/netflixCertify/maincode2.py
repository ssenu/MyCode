import imaplib
import email
from email.header import decode_header, make_header
from bs4 import BeautifulSoup
import webbrowser
import base64
def extract_body(msg):
    text_body = None
    html_body = None

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            dispo = str(part.get("Content-Disposition"))

            if "attachment" in dispo:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            if ctype == "text/plain":
                text_body = payload.decode(errors="ignore")

            elif ctype == "text/html":
                html_body = payload.decode(errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text_body = payload.decode(errors="ignore")

    return text_body or html_body or ""

# 메일 아이디 / 비밀번호(앱 비밀번호 : 구글 발급)
EMAIL_ID = "cwhappy123@gmail.com"
EMAIL_PW = "rujwjlmjkjvnrbgg"

mailTitle = input("검색할 단어(ex. 코드) : ")

server = imaplib.IMAP4_SSL('imap.gmail.com')
server.login(EMAIL_ID, EMAIL_PW)
server.select("INBOX")
rv, data = server.select()
# 연결 확인
print("연결확인 :", rv)
print("메일개수 :", int(data[0].decode()))


# 체크할 메일 수
num = 10

print(f"최근 메일 중 총 {num} 개의 메일에 '{mailTitle}' 단어 포함 체크")


for i in range(0, num, 1):
    print(f"{i+1}번째 메일 확인중..", end="")
    mailnum = str(int(data[0].decode()) - i).encode()
    rv, fetched = server.fetch(mailnum, '(RFC822)')
    message = email.message_from_bytes(fetched[0][1])
    subject = make_header(decode_header(message.get('Subject')))
    decoded_parts = decode_header(str(subject))

    decoded_text = ""
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            decoded_text += part.decode(charset or "utf-8", errors="ignore")
        else:
            decoded_text += part

    if mailTitle in decoded_text:
        print("\n")
        break
    print("X")


#보낸사람
fr = make_header(decode_header(message.get('From')))
print("메일 제목 :", subject)
print("보낸사람 :", fr)

html_body = None
text_body = None

body = None

def extract_body(msg):
    text_body = None
    html_body = None

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            dispo = str(part.get("Content-Disposition"))

            if "attachment" in dispo:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            if ctype == "text/plain":
                text_body = payload.decode(errors="ignore")

            elif ctype == "text/html":
                html_body = payload.decode(errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text_body = payload.decode(errors="ignore")

    return text_body or html_body or ""

print(f"내용:{body}")


if message.is_multipart():
    for part in message.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

        if 'attachment' in cdispo:
            continue

        if ctype == 'text/plain':
            text_body = part.get_payload(decode=True)

        elif ctype == 'text/html':
            html_body = part.get_payload(decode=True)

else:
    text_body = message.get_payload(decode=True)

if html_body:
    body = html_body.decode('utf-8', errors='ignore')
elif text_body:
    body = text_body.decode('utf-8', errors='ignore')
else:
    body = ""
body = extract_body(message)


html = body

soup = BeautifulSoup(html, "html.parser")



# HTML을 base64로 인코딩
encoded_html = base64.b64encode(body.encode("utf-8")).decode("utf-8")

# data URL 생성
data_url = f"data:text/html;base64,{encoded_html}"

# 크롬으로 열기
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(chrome_path).open(data_url)
