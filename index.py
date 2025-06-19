from flask import Flask, request, render_template_string
import smtplib
import ssl

app = Flask(__name__)

# Gmail ayarları
EMAIL_GONDEREN = "seningmail@gmail.com"
EMAIL_SIFRE = "uygulama_sifresi"
EMAIL_ALICI = "seningmail@gmail.com"

# HTML FORM KODU (direkt Python içinde)
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Mesaj Gönder</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Mesajını Gönder</h1>
    <form method="POST" action="/">
        <input type="text" name="isim" placeholder="Adınız" required><br><br>
        <textarea name="mesaj" placeholder="Mesajınızı yazınız" rows="5" cols="30" required></textarea><br><br>
        <button type="submit">Gönder</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def mesaj():
    if request.method == "POST":
        isim = request.form["isim"]
        mesaj = request.form["mesaj"]
        icerik = f"{isim} adlı kişiden mesaj:\n\n{mesaj}"

        # Mail gönderimi
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(EMAIL_GONDEREN, EMAIL_SIFRE)
                server.sendmail(
                    EMAIL_GONDEREN,
                    EMAIL_ALICI,
                    f"Subject: Web Mesajı\n\n{icerik}"
                )
            return "✅ Mesaj başarıyla gönderildi!"
        except Exception as e:
            return f"❌ Hata oluştu: {e}"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(debug=True)
