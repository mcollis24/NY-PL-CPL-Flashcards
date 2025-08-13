
from flask import Flask, render_template, send_from_directory
import random, os, argparse

app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")

penal_law = {
    "Article 10: Definitions": {"Sections": "§§ 10.00","Summary": "Legal definitions essential for interpreting the law"},
    "Article 15: Culpable Mental States": {"Sections": "§§ 15.00-15.25","Summary": "Intent, knowledge, recklessness, criminal negligence"},
    "Article 20: Accessorial Liability": {"Sections": "§§ 20.00","Summary": "Liability for aiding or abetting crimes"},
    "Article 35: Justification": {"Sections": "§§ 35.00-35.30","Summary": "Use of physical or deadly force"},
    "Article 70: Sentencing": {"Sections": "§§ 70.00-70.45","Summary": "Sentencing ranges for felonies and misdemeanors"},
    "Article 120: Assault and Related Offenses": {"Sections": "§§ 120.00-120.60","Summary": "Assault, reckless endangerment, etc"},
    "Article 125: Homicide": {"Sections": "§§ 125.00-125.60","Summary": "Murder, manslaughter, criminally negligent homicide"},
    "Article 130: Sex Offenses": {"Sections": "§§ 130.00-130.96","Summary": "Rape, sexual abuse, etc."},
    "Article 140: Burglary and Trespass": {"Sections": "§§ 140.00-140.40","Summary": "Unlawful entry-related offenses"},
    "Article 145: Criminal Mischief": {"Sections": "§§ 145.00-145.40","Summary": "Damage to property"},
    "Article 155: Larceny": {"Sections": "§§ 155.00-155.45","Summary": "Theft and related charges"},
    "Article 160: Robbery": {"Sections": "§§ 160.00-160.15","Summary": "Forcible stealing"},
    "Article 165: Possession of Stolen Property": {"Sections": "§§ 165.00-165.55","Summary": "Knowingly possessing stolen goods"},
    "Article 205: Resisting Arrest, Escape": {"Sections": "§§ 205.00-205.70","Summary": "Obstructing law enforcement"},
    "Article 215: Obstruction, Witness Intimidation": {"Sections": "§§ 215.00-215.56","Summary": "Obstructing governmental administration"},
    "Article 220: Controlled Substances": {"Sections": "§§ 220.00-220.65","Summary": "Drug possession and sale"},
    "Article 240: Disorderly Conduct, Harassment": {"Sections": "§§ 240.00-240.75","Summary": "Public order offenses"},
    "Article 260: Offenses Relating to Children": {"Sections": "§§ 260.00-260.35","Summary": "Child endangerment"},
    "Article 265: Firearms and Dangerous Weapons": {"Sections": "§§ 265.00-265.66","Summary": "Gun and weapon laws"}
}

criminal_procedure_law = {
    "Article 1: General Provisions": {"Sections": "§§ 1.00-1.20","Summary": "Definitions and general rules"},
    "Article 2: Peace Officers": {"Sections": "§ 2.10","Summary": "List of peace officer titles"},
    "Article 10: Jurisdiction": {"Sections": "§§ 10.00-10.40","Summary": "Which courts have authority over criminal matters"},
    "Article 30: Timeliness of Prosecution": {"Sections": "§§ 30.10-30.30","Summary": "Statutes of limitations and speedy trial"},
    "Article 100: Accusatory Instruments": {"Sections": "§§ 100.00-100.55","Summary": "Complaints, informations, simplified traffic infos"},
    "Article 120: Arrest Warrants": {"Sections": "§§ 120.00-120.90","Summary": "Procedures for issuing and executing warrants"},
    "Article 130: Appearance Tickets": {"Sections": "§§ 130.00-130.60","Summary": "Written notice to appear in court"},
    "Article 140: Arrest Without Warrant": {"Sections": "§§ 140.00-140.55","Summary": "When police can arrest without a warrant"},
    "Article 150: Summonses": {"Sections": "§§ 150.00-150.75","Summary": "Court orders to appear"},
    "Article 160: Booking Procedures": {"Sections": "§§ 160.00-160.60","Summary": "Fingerprints, photographs"},
    "Article 170: Local Court Proceedings": {"Sections": "§§ 170.00-170.85","Summary": "How misdemeanors and violations proceed"},
    "Article 180: Felony Hearings": {"Sections": "§§ 180.00-180.85","Summary": "Preliminary hearings in felony cases"},
    "Article 240: Discovery": {"Sections": "§§ 240.10-240.90","Summary": "Exchange of evidence before trial"}
}

def build_flashcards():
    cards = []
    for key, value in penal_law.items():
        cards.append({"summary": value["Summary"], "article": key, "sections": value["Sections"], "law": "Penal Law"})
    for key, value in criminal_procedure_law.items():
        cards.append({"summary": value["Summary"], "article": key, "sections": value["Sections"], "law": "Criminal Procedure Law"})
    return cards

@app.route("/")
def index():
    cards = build_flashcards()
    return render_template("index.html", flashcards=cards)

@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(app.static_folder, "service-worker.js", mimetype="application/javascript")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)))
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port, debug=True)
