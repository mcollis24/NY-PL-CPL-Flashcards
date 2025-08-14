
from flask import Flask, render_template, send_from_directory
import os, argparse

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

environmental_conservation_law = {
    "Article 1: General Provisions": {"Sections": "§§ 1.00", "Summary": "Foundational policy and definitions across ECL"},
    "Article 3: Department of Environmental Conservation": {"Sections": "§§ 3.01-3.52", "Summary": "Establishes the powers and duties of the DEC"},
    "Article 6: Smart Growth Infrastructure": {"Sections": "§§ 6.00", "Summary": "Promotes sustainable and efficient infrastructure development"},
    "Article 8: Environmental Quality Review (SEQRA)": {"Sections": "§§ 8.0101-8.0117", "Summary": "Requires environmental impact reviews for government actions"},
    "Article 9: Lands and Forests": {"Sections": "§§ 9.01-9.55", "Summary": "Manages state forests, reforestation, and timber use"},
    "Article 11: Fish and Wildlife": {"Sections": "§§ 11.01-11.55", "Summary": "Regulates wildlife, fishing, hunting, and trapping"},
    "Article 13: Marine and Coastal Resources": {"Sections": "§§ 13.01-13.45", "Summary": "Covers coastal and marine habitat conservation"},
    "Article 15: Water Resources": {"Sections": "§§ 15.01-15.55", "Summary": "Regulates surface and groundwater use and conservation"},
    "Article 17: Water Pollution Control": {"Sections": "§§ 17.01-17.55", "Summary": "Sets water quality standards and discharge permits"},
    "Article 19: Air Pollution Control": {"Sections": "§§ 19.01-19.55", "Summary": "Regulates air quality and emissions standards"},
    "Article 23: Mineral Resources": {"Sections": "§§ 23.01-23.55", "Summary": "Covers mining permits, reclamation, and oil/gas drilling"},
    "Article 24: Freshwater Wetlands": {"Sections": "§§ 24.01-24.55", "Summary": "Protects freshwater wetlands through permits and restrictions"},
    "Article 25: Tidal Wetlands": {"Sections": "§§ 25.01-25.55", "Summary": "Regulates activities affecting coastal and tidal wetlands"},
    "Article 27: Solid Waste Management": {"Sections": "§§ 27.01-27.71", "Summary": "Governs waste disposal, recycling, and landfill regulations"},
    "Article 33: Pesticides": {"Sections": "§§ 33.01-33.55", "Summary": "Regulates sale, use, and disposal of pesticides"},
    "Article 37: Hazardous Substances": {"Sections": "§§ 37.01-37.55", "Summary": "Lists and controls dangerous chemical substances"},
    "Article 75: Climate Change Mitigation": {"Sections": "§§ 75.01-75.55", "Summary": "Establishes statewide emissions limits and carbon reduction goals"}
}

def build_quiz_sets():
    def pack(d, name):
        return [{"summary": v["Summary"], "article": k, "sections": v["Sections"], "law": name} for k, v in d.items()]
    return {
        "Penal Law": pack(penal_law, "Penal Law"),
        "Criminal Procedure Law": pack(criminal_procedure_law, "Criminal Procedure Law"),
        "Environmental Conservation Law": pack(environmental_conservation_law, "Environmental Conservation Law"),
    }

def build_browse_list():
    items = []
    for k, v in penal_law.items():
        items.append({"summary": v["Summary"], "article": k, "sections": v["Sections"], "law": "Penal Law"})
    for k, v in criminal_procedure_law.items():
        items.append({"summary": v["Summary"], "article": k, "sections": v["Sections"], "law": "Criminal Procedure Law"})
    for k, v in environmental_conservation_law.items():
        items.append({"summary": v["Summary"], "article": k, "sections": v["Sections"], "law": "Environmental Conservation Law"})
    return items

@app.route("/")
def index():
    return render_template("index.html",
                           quiz_sets=build_quiz_sets(),
                           browse_items=build_browse_list())

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
