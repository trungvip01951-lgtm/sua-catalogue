import openpyxl
for dn, cuc, n in (('150', 2, 2900), ('200', 4, 1450)):
    wb = openpyxl.load_workbook('WCL.xlsx')
    for r in wb['THONG_TIN'].iter_rows(min_row=2):
        if r[0].value == 'so_cuc': r[1].value = cuc
        if r[0].value == 'toc_do_vg_ph': r[1].value = n
    for sh, col in (('MODEL', 2), ('QH', 1)):
        ws = wb[sh]
        for i in range(ws.max_row, 1, -1):
            if not str(ws.cell(i, col + 1).value).startswith(dn + 'WC'): ws.delete_rows(i)
    wb.save(f'WCL_{dn}.xlsx')
