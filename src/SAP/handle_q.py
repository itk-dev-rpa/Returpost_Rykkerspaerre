from itk_dev_shared_components.sap import gridview_util

def handle_Q(session):
    case_table = session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell')
    gridview_util.scroll_entire_table(case_table, True)

    for row in range(case_table.RowCount):
        if row > 3:
            break
        
        # Open case
        case_table.doubleClick(row, 'ZZ_IDNUMBER')

        # Open aftaleindhold
        session.findById("wnd[0]/usr/tabsTABSTRIP/tabpBUTOBJ").select()
        afklaring_table = session.findById('wnd[0]/usr/tabsTABSTRIP/tabpBUTOBJ/ssubTABSUB:SAPLEMMA_CASE_TRANSACTION:0210/cntlWORKAREA1/shellcont/shell')
        row_index = gridview_util.find_row_index_by_value(afklaring_table, 'CELEMNAME', 'Aftaleindhold')
        afklaring_table.setCurrentCell(row_index, 'ID')
        afklaring_table.clickCurrentCell()

        # Press edit, delete 'Q' and save
        if session.findById("wnd[0]/usr/subBDT_AREA:SAPLBUSS:0021/tabsBDT_TABSTRIP01/tabpBUSCR02_01/ssubGENSUB:SAPLBUSS:0029/ssubGENSUB:SAPLBUSS:7135/subA04P02:SAPLFMCA_PSOB_BDT2:0330/ctxtSPSOB_SCR_2110_H3-DUNN_REASON").text == 'Q':
            session.findById("wnd[0]/usr/btnPUSHB_CHANGE").press()
            session.findById("wnd[0]/usr/subBDT_AREA:SAPLBUSS:0021/tabsBDT_TABSTRIP01/tabpBUSCR02_01").select()
            session.findById("wnd[0]/usr/subBDT_AREA:SAPLBUSS:0021/tabsBDT_TABSTRIP01/tabpBUSCR02_01/ssubGENSUB:SAPLBUSS:0029/ssubGENSUB:SAPLBUSS:7135/subA04P02:SAPLFMCA_PSOB_BDT2:0330/ctxtSPSOB_SCR_2110_H3-DUNN_REASON").text = ""
            session.findById("wnd[0]/tbar[0]/btn[11]").press()
        else:
            session.findById('wnd[0]/tbar[0]/btn[3]').press()

        # Set status to 'Afsluttet and save
        session.findById("wnd[0]/usr/cmbEMMAD_CASEHDR-STATUS").value = "Afsluttet"
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
