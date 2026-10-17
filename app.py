from flask import Flask, request, render_template_string

app = Flask(__name__)

MENUS = [
    {"nama": "Ayam Geprek", "harga": 20000, "kategori": "Makanan", "rasa": "Pedas"},
    {"nama": "Nasi Goreng", "harga": 15000, "kategori": "Makanan", "rasa": "Gurih"},
    {"nama": "Mie Ayam", "harga": 12000, "kategori": "Makanan", "rasa": "Gurih"},
    {"nama": "Seblak", "harga": 15000, "kategori": "Makanan", "rasa": "Pedas"},
    {"nama": "Es Teh", "harga": 5000, "kategori": "Minuman", "rasa": "Manis"},
    {"nama": "Jus Alpukat", "harga": 10000, "kategori": "Minuman", "rasa": "Manis"},
]

HALAMAN = """
<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#166534">
<title>SmartKuliner</title>
<style>
body{font-family:Arial,sans-serif;background:#f0fdf4;margin:0;color:#183323}
header{background:#166534;color:white;padding:25px 16px;text-align:center}
main{max-width:720px;margin:22px auto;padding:0 14px}
.kartu{background:white;padding:18px;border-radius:14px;margin-bottom:14px;box-shadow:0 2px 8px #0001}
label{display:block;margin:12px 0 6px}
select,button{box-sizing:border-box;width:100%;padding:12px;border-radius:8px;font-size:16px}
select{border:1px solid #aaa;background:white}
button{background:#166534;color:white;border:0;margin-top:18px;font-weight:bold}
.menu{display:flex;justify-content:space-between;gap:10px;border-bottom:1px solid #eee;padding:12px 0}
.harga{color:#166534;font-weight:bold;white-space:nowrap}
small{color:#64748b}
</style>
</head>
<body>
<header>
<h1>🍽️ SmartKuliner</h1>
<p>Temukan menu sesuai selera dan anggaranmu!</p>
</header>
<main>
<section class="kartu">
<h2>Rekomendasi Menu</h2>
<form method="get">
<label for="rasa">Pilih rasa favorit</label>
<select id="rasa" name="rasa">
{% for r in ["Semua", "Pedas", "Gurih", "Manis"] %}
<option value="{{r}}" {% if rasa == r %}selected{% endif %}>{{r}}</option>
{% endfor %}
</select>
<label for="kategori">Jenis menu</label>
<select id="kategori" name="kategori">
{% for k in ["Semua", "Makanan", "Minuman"] %}
<option value="{{k}}" {% if kategori == k %}selected{% endif %}>{{k}}</option>
{% endfor %}
</select>
<label for="budget">Anggaran maksimal</label>
<select id="budget" name="budget">
{% for b in [10000, 15000, 20000, 50000] %}
<option value="{{b}}" {% if budget == b %}selected{% endif %}>Rp{{"{:,.0f}".format(b).replace(",",".")}}</option>
{% endfor %}
</select>
<button type="submit">Cari Rekomendasi</button>
</form>
</section>
<section class="kartu">
<h2>Menu yang Cocok untukmu</h2>
{% if hasil %}
{% for m in hasil %}
<div class="menu">
<div><strong>{{m.nama}}</strong><br><small>{{m.kategori}} · {{m.rasa}}</small></div>
<div class="harga">Rp{{"{:,.0f}".format(m.harga).replace(",",".")}}</div>
</div>
{% endfor %}
{% else %}
<p>Belum ada menu yang cocok. Coba ubah pilihanmu.</p>
{% endif %}
</section>
<p><small>SmartKuliner · Sistem rekomendasi menu berbasis preferensi pelanggan.</small></p>
</main>
</body>
</html>
"""

@app.route("/")
def beranda():
    rasa = request.args.get("rasa", "Semua")
    kategori = request.args.get("kategori", "Semua")
    try:
        budget = int(request.args.get("budget", "20000"))
    except ValueError:
        budget = 20000

    if rasa not in ["Semua", "Pedas", "Gurih", "Manis"]:
        rasa = "Semua"
    if kategori not in ["Semua", "Makanan", "Minuman"]:
        kategori = "Semua"

    hasil = [
        m for m in MENUS
        if (rasa == "Semua" or m["rasa"] == rasa)
        and (kategori == "Semua" or m["kategori"] == kategori)
        and m["harga"] <= budget
    ]

    return render_template_string(
        HALAMAN, hasil=hasil, rasa=rasa,
        kategori=kategori, budget=budget
    )

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5055)
