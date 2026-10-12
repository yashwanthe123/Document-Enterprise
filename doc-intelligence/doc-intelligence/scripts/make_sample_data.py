"""Generate a small synthetic PDF corpus so the pipeline can be tried
without any real (confidential) documents.

    python scripts/make_sample_data.py --n 30
"""
import argparse
import random
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

CATEGORIES = ["invoice", "contract", "resume", "report"]

COMPANIES = ["Nandi Steels", "Kaveri Logistics", "Bluepeak Systems", "Orbit Analytics",
             "Malnad Foods", "Sahyadri Infra", "Lumen Retail", "Vertex Labs"]
NAMES = ["Arjun Rao", "Meera Iyer", "Karthik Shetty", "Divya Nair", "Rohan Gowda", "Sneha Pai"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def date(r):
    return f"{r.randint(1, 28)} {r.choice(MONTHS)} {r.randint(2022, 2025)}"


def invoice(r):
    items = r.sample(["steel rods", "freight charges", "cloud hosting", "consulting hours",
                      "packaging", "warehouse rent", "software licence", "maintenance"], 4)
    lines = [f"INVOICE  INV-{r.randint(1000, 9999)}", f"Invoice date: {date(r)}   Due date: {date(r)}",
             f"Billed to: {r.choice(COMPANIES)}", f"Vendor: {r.choice(COMPANIES)}",
             "Description  Quantity  Unit price  Amount"]
    total = 0
    for it in items:
        q, p = r.randint(1, 20), r.randint(200, 9000)
        total += q * p
        lines.append(f"{it}  {q}  Rs. {p}  Rs. {q * p}")
    lines += [f"Subtotal: Rs. {total}", f"GST 18% payable: Rs. {int(total * .18)}",
              f"Total amount due: Rs. {int(total * 1.18)}",
              "Payment terms: net 30 days. Bank transfer to the account listed. Late payment attracts interest.",
              f"Contact: accounts@{r.choice(COMPANIES).split()[0].lower()}.com"]
    return lines


def contract(r):
    a, b = r.sample(COMPANIES, 2)
    return [f"SERVICE AGREEMENT", f"This agreement is entered into on {date(r)} between {a} and {b}.",
            "1. Scope of services. The service provider shall deliver the services described in Schedule A.",
            "2. Term and termination. Either party may terminate this agreement with sixty days written notice.",
            "3. Confidentiality. Both parties agree to keep confidential information strictly confidential.",
            "4. Liability and indemnity. The provider indemnifies the client against third party claims.",
            "5. Governing law. This agreement is governed by the laws of India; disputes go to arbitration in Bengaluru.",
            "6. Intellectual property. All deliverables remain the property of the client upon full payment.",
            f"Signed by {r.choice(NAMES)} and {r.choice(NAMES)}. Witness clause and jurisdiction apply."]


def resume(r):
    skills = r.sample(["Python", "Java", "SQL", "React", "machine learning", "Docker", "Excel",
                       "project management", "AWS", "communication"], 5)
    return [r.choice(NAMES), f"Email: {r.choice(NAMES).split()[0].lower()}@mail.com   Phone: 9{r.randint(100000000, 999999999)}",
            "Objective: seeking a challenging role to apply my skills and grow professionally.",
            "Education: B.E. Computer Science, BMS College of Engineering, CGPA 8.%d" % r.randint(0, 9),
            f"Experience: intern at {r.choice(COMPANIES)}, worked on backend services and data pipelines.",
            "Skills: " + ", ".join(skills),
            "Projects: built a web application and a classification model as part of coursework.",
            "Achievements: led a student club, organised events, won a hackathon.",
            "Certifications: completed online courses in cloud and databases. References available on request."]


def report(r):
    topic = r.choice(["supply chain performance", "customer churn", "energy consumption", "warehouse safety"])
    return [f"Quarterly Report: {topic}", f"Prepared by {r.choice(NAMES)}, {date(r)}",
            f"Executive summary. This report analyses {topic} over the last quarter and highlights key trends.",
            "Methodology. Data was collected from internal systems and analysed using statistical methods.",
            f"Findings. We observed a {r.randint(3, 25)}% change compared to the previous quarter; variance was driven by seasonal demand.",
            "Discussion. The results suggest several areas for improvement and further investigation.",
            "Recommendations. Invest in monitoring, review processes, and revisit targets next quarter.",
            "Conclusion. Overall performance is stable, with risks noted in the appendix and figures."]


MAKERS = {"invoice": invoice, "contract": contract, "resume": resume, "report": report}


def write_pdf(path, lines):
    c = canvas.Canvas(str(path), pagesize=A4)
    y = 800
    for line in lines:
        c.drawString(50, y, line[:110])
        y -= 22
    c.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30, help="documents per category")
    ap.add_argument("--out", default="data/raw")
    args = ap.parse_args()

    r = random.Random(42)
    for cat, maker in MAKERS.items():
        d = Path(args.out) / cat
        d.mkdir(parents=True, exist_ok=True)
        for i in range(args.n):
            write_pdf(d / f"{cat}_{i:03d}.pdf", maker(r))
    print(f"wrote {args.n * len(MAKERS)} pdfs to {args.out}")


if __name__ == "__main__":
    main()
