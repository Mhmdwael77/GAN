from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


report_date = date.today().isoformat()
output_file = "ML_Pipeline_Bugfix_Report.pdf"

lines = [
    "ML Pipeline YAML Bug Fix Report",
    f"Date: {report_date}",
    "",
    "1) Objective",
    "Move from manual validation to automated CI by fixing and completing the GitHub Actions pipeline.",
    "",
    "2) Bugs Found in Provided YAML",
    "- Bug 1: Incorrect YAML indentation under on, push, branches, jobs, and steps.",
    "- Bug 2: Trigger did not satisfy requirement; it targeted main instead of all branches except main.",
    "- Bug 3: Linter Check step had no uses or run command.",
    "- Bug 4: Missing repository checkout step before workflow operations.",
    "- Bug 5: Missing artifact upload step for README.md.",
    "",
    "3) Fixes Applied",
    "- Fix 1: Corrected YAML indentation across all workflow sections.",
    "- Fix 2: Updated trigger to push on all branches except main with branches-ignore.",
    "- Fix 3: Added Ruff linter execution in Linter Check step.",
    "- Fix 4: Added actions/checkout@v4 as first step.",
    "- Fix 5: Added actions/upload-artifact@v4 with artifact name project-doc and path README.md.",
    "",
    "4) Required Evidence",
    "- Public repository link: https://github.com/Mhmdwael77/GAN",
    "- Successful workflow run (green): https://github.com/Mhmdwael77/GAN/actions/runs/23101955047",
    "- Screenshot evidence: Attached GitHub Actions screenshot shows ML Model CI status = Success.",
    "",
    "5) Updated Workflow File",
    "- .github/workflows/ml-pipeline.yml",
]

pdf = canvas.Canvas(output_file, pagesize=A4)
width, height = A4
left_margin = 50
top_margin = height - 50
line_height = 16
y = top_margin

for line in lines:
    if y < 50:
        pdf.showPage()
        y = top_margin
    if line == "ML Pipeline YAML Bug Fix Report":
        pdf.setFont("Helvetica-Bold", 16)
    elif len(line) > 3 and line[0].isdigit() and line[1] == ")":
        pdf.setFont("Helvetica-Bold", 12)
    else:
        pdf.setFont("Helvetica", 11)
    pdf.drawString(left_margin, y, line)
    y -= line_height

pdf.save()
print(f"Generated {output_file}")
