import pandas as pd
from fpdf import FPDF

def export_par_sheet():
    # Load simulation data
    try:
        df = pd.read_csv("summary.csv")
    except FileNotFoundError:
        print("summary.csv not found. Run the simulation first.")
        return

    # --- Export to Excel ---
    excel_file = "summary_export.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"✅ Exported to Excel: {excel_file}")

    # --- Export to PDF ---
    pdf_file = "summary_report.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BuffaloLite PAR Sheet Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    # RTP & summary stats
    total_spins = len(df)
    total_win = df["WinAmount"].sum()
    rtp = total_win / total_spins
    pdf.cell(0, 10, f"Total Spins: {total_spins}", ln=True)
    pdf.cell(0, 10, f"Total Win: {total_win:.2f}", ln=True)
    pdf.cell(0, 10, f"RTP: {rtp:.4f}", ln=True)
    pdf.ln(10)

    # Symbol-wise report
    grouped = df.groupby("WinningSymbol")["WinAmount"].agg(["count", "sum"])
    grouped["RTP"] = grouped["sum"] / total_spins

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Symbol", 1)
    pdf.cell(40, 10, "Hits", 1)
    pdf.cell(40, 10, "Win Sum", 1)
    pdf.cell(40, 10, "RTP", 1)
    pdf.ln()

    pdf.set_font("Arial", size=11)
    for index, row in grouped.iterrows():
        pdf.cell(40, 10, str(index), 1)
        pdf.cell(40, 10, str(int(row['count'])), 1)
        pdf.cell(40, 10, f"{row['sum']:.2f}", 1)
        pdf.cell(40, 10, f"{row['RTP']:.4f}", 1)
        pdf.ln()

    pdf.output(pdf_file)
    print(f"✅ Exported to PDF: {pdf_file}")

if __name__ == "__main__":
    export_par_sheet()
