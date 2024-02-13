"""This module handles all Rykkerspærre of type 'Q'."""

from itk_dev_shared_components.sap import gridview_util

from . import common


def handle_q(session):
    """Handle all Rykkerspærre of type 'Q'."""
    case_table = session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell')
    gridview_util.scroll_entire_table(case_table, True)

    for row in range(case_table.RowCount):
        common.open_aftaleindhold(session, case_table, row)

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
