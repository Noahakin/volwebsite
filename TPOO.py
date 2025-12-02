import pandas as pd
import numpy as np
import xlsxwriter

# === CONFIGURATION ===
input_file = "Book4.xlsx"   # Ensure this file is in the same folder
advisor_name = "Armis Advisers"
output_file = "Armis_Advisers_Client_Reports_PriorNotional_Final.xlsx"

# === LOAD DATA ===
df = pd.read_excel(input_file, sheet_name="Table2")
df = df[df["Advisor"] == advisor_name].copy()
df["Fee"] = pd.to_numeric(df["Fee"], errors="coerce").fillna(0)

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October"]
month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct"]

def compound_return(returns):
    returns = np.nan_to_num(returns, nan=0.0, posinf=0.0, neginf=0.0)
    return np.prod([(1 + r) for r in returns]) - 1

# === START WORKBOOK ===
wb = xlsxwriter.Workbook(output_file)

# === FORMATS ===
title_fmt = wb.add_format({'bold': True, 'font_size': 14, 'align': 'center',
                           'valign': 'vcenter', 'bg_color': '#305496', 'font_color': 'white'})
header_fmt = wb.add_format({'bold': True, 'bg_color': '#D9E1F2', 'align': 'center', 'border': 1})
label_fmt = wb.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1})
value_fmt = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
section_hdr = wb.add_format({'bold': True, 'align': 'center', 'bg_color': '#D9E1F2', 'border': 1})
gross_hdr = wb.add_format({'bold': True, 'bg_color': '#8EA9DB', 'align': 'center', 'border': 1})
net_hdr = wb.add_format({'bold': True, 'bg_color': '#F4B083', 'align': 'center', 'border': 1})
alt1, alt2 = '#F2F2F2', '#FFFFFF'

# === TRACK SHEETS FOR SUMMARY ===
sheet_refs = []

# === CREATE ONE SHEET PER ACCOUNT ===
for (client_name, acct_num), group in df.groupby(["Account Name", "Account Number"]):
    # Generate safe sheet name
    sheet_name = f"{client_name[:20]}_{str(acct_num)[-3:]}"
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:31]
    ws = wb.add_worksheet(sheet_name)
    ws.hide_gridlines(2)
    sheet_refs.append((client_name, acct_num, sheet_name))

    # Extract data safely
    fee = float(group["Fee"].iloc[0])
    custodian = group["Custodian"].iloc[0]
    gl_last = np.nan_to_num(group.loc[group["G/L"] == "G/L $ (Last Month)", months].values[0].astype(float), nan=0.0)
    gl_pct = np.nan_to_num(group.loc[group["G/L"] == "G/L %", months].values[0].astype(float), nan=0.0)
    notional = np.nan_to_num(group.loc[group["G/L"] == "Notional", months].values[0].astype(float), nan=0.0)
    prior_notional_base = group.loc[group["G/L"] == "Notional", "Column6"].values[0] if "Column6" in group.columns else notional[0]

    # Build monthly data
    monthly = pd.DataFrame({"Month": month_abbr})
    monthly["Gross G/L $"] = gl_last
    monthly["Gross G/L %"] = gl_pct
    monthly["Net G/L %"] = monthly["Gross G/L %"] - (fee / 12)
    prior_notional = [prior_notional_base] + list(notional[:-1])
    monthly["Net G/L $"] = np.array(prior_notional) * monthly["Net G/L %"]

    # Quarterly + YTD
    quarters = {"Q1": monthly.iloc[0:3], "Q2": monthly.iloc[3:6],
                "Q3": monthly.iloc[6:9], "Q4": monthly.iloc[9:10]}
    q_summary = []
    for q, data in quarters.items():
        gross_sum = data["Gross G/L $"].sum()
        net_sum = data["Net G/L $"].sum()
        gross_comp = compound_return(data["Gross G/L %"].values)
        net_comp = compound_return(data["Net G/L %"].values)
        q_summary.append([q, gross_sum, gross_comp, net_sum, net_comp])

    ytd_gross = monthly["Gross G/L $"].sum()
    ytd_net = monthly["Net G/L $"].sum()
    ytd_gross_pct = compound_return(monthly["Gross G/L %"].values)
    ytd_net_pct = compound_return(monthly["Net G/L %"].values)
    q_summary.append(["YTD", ytd_gross, ytd_gross_pct, ytd_net, ytd_net_pct])
    qdf = pd.DataFrame(q_summary, columns=["Period", "Gross G/L $", "Gross G/L %", "Net G/L $", "Net G/L %"])

    # HEADER
    ws.merge_range("B2:F2", f"Performance Report — {client_name}", title_fmt)
    info = [
        ("Account Number", acct_num),
        ("Account Name", client_name),
        ("Custodian", custodian),
        ("Advisor", advisor_name),
        ("Liquid Strategies Fee % (Annual)", fee)
    ]
    for i, (k, v) in enumerate(info):
        r = 3 + i
        ws.write(r, 1, k, label_fmt)
        fmt = wb.add_format({'num_format': '0.00%', 'align': 'center', 'valign': 'vcenter', 'border': 1}) if "Fee" in k else value_fmt
        ws.merge_range(r, 2, r, 3, v, fmt)

    # MONTHLY SUMMARY
    ws.merge_range("B10:F10", "Monthly Summary", section_hdr)
    headers = ["Month", "Gross G/L $", "Gross G/L %", "Net G/L $", "Net G/L %"]
    hdrs = [header_fmt, gross_hdr, gross_hdr, net_hdr, net_hdr]
    for c, h in enumerate(headers):
        ws.write(10, c + 1, h, hdrs[c])

    for i, row in enumerate(monthly.itertuples(), start=11):
        color = alt1 if i % 2 == 0 else alt2
        fmt1 = wb.add_format({'bg_color': color, 'border': 1, 'align': 'left'})
        fmt2 = wb.add_format({'bg_color': color, 'border': 1, 'align': 'right', 'num_format': '$#,##0.00'})
        fmt3 = wb.add_format({'bg_color': color, 'border': 1, 'align': 'right', 'num_format': '0.00%'})
        ws.write(i, 1, row.Month, fmt1)
        ws.write(i, 2, row._2, fmt2)
        ws.write(i, 3, row._3, fmt3)
        ws.write(i, 4, row._5, fmt2)
        ws.write(i, 5, row._4, fmt3)

    # QUARTERLY + YTD
    s = 24
    ws.merge_range(s, 1, s, 5, "Quarterly and YTD Summary", section_hdr)
    for c, h in enumerate(headers):
        ws.write(s + 1, c + 1, h, hdrs[c])

    for i, row in enumerate(qdf.itertuples(), start=s + 2):
        color = alt1 if i % 2 == 0 else alt2
        border_top = 2 if row.Period == "YTD" else 1
        bold = True if row.Period == "YTD" else False
        fmt2b = wb.add_format({'bg_color': color, 'border': border_top, 'bold': bold,
                               'align': 'right', 'num_format': '$#,##0.00'})
        fmt3b = wb.add_format({'bg_color': color, 'border': border_top, 'bold': bold,
                               'align': 'right', 'num_format': '0.00%'})
        fmt1b = wb.add_format({'bg_color': color, 'border': border_top, 'bold': bold, 'align': 'left'})
        ws.write(i, 1, row.Period, fmt1b)
        ws.write(i, 2, row._2, fmt2b)
        ws.write(i, 3, row._3, fmt3b)
        ws.write(i, 4, row._4, fmt2b)
        ws.write(i, 5, row._5, fmt3b)

    ws.set_column(1, 5, 18)

# === SUMMARY SHEET ===
summary = wb.add_worksheet("Summary")
summary.write_row("B2", ["Client Name", "Account Number", "Link to Sheet"], header_fmt)

for idx, (client_name, acct_num, sheet_name) in enumerate(sheet_refs, start=3):
    link = f"internal:'{sheet_name}'!B2"
    summary.write(idx, 1, client_name, value_fmt)
    summary.write(idx, 2, acct_num, value_fmt)
    summary.write_url(idx, 3, link, wb.add_format({'font_color': 'blue', 'underline': 1}), string="Go to Sheet")

summary.set_column(1, 3, 30)

wb.close()
print(f"✅ Finished! File saved as {output_file}")
