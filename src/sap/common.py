"""This module contains common functionality regarding the SAP process."""

from itk_dev_shared_components.sap import gridview_util


def open_afklaringsliste(session):
    """Open the afklaringsliste in emmacl and apply the correct filters."""
    session.findById("wnd[0]/tbar[0]/okcd").text = "emmacl"
    session.findById("wnd[0]").sendVKey(0)
    session.findById("wnd[0]/tbar[1]/btn[17]").press()
    session.findById("wnd[1]/usr/txtV-LOW").text = "standard"
    session.findById("wnd[1]/usr/txtENAME-LOW").text = ""
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/tbar[1]/btn[8]").press()


def select_layout(session, layout: str):
    """Set the layout of the afklaringsliste to the given layout name"""
    session.findById("wnd[0]/tbar[1]/btn[33]").press()
    layout_table = session.findById("wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell")
    row_index = gridview_util.find_row_index_by_value(layout_table, "VARIANT", layout)
    layout_table.setCurrentCell(row_index, 'VARIANT')
    layout_table.clickCurrentCell()


def open_aftaleindhold(session, case_table, row_index: int) -> None:
    """Opens the aftaleindhold of the case on the given row of the given table."""
    # Select row and click 'Ændr'
    case_table.firstVisibleRow = row_index
    case_table.selectedRows = row_index
    session.findById("wnd[0]/tbar[1]/btn[14]").press()

    # Open aftaleindhold
    session.findById("wnd[0]/usr/tabsTABSTRIP/tabpBUTOBJ").select()
    afklaring_table = session.findById('wnd[0]/usr/tabsTABSTRIP/tabpBUTOBJ/ssubTABSUB:SAPLEMMA_CASE_TRANSACTION:0210/cntlWORKAREA1/shellcont/shell')
    row_index = gridview_util.find_row_index_by_value(afklaring_table, 'CELEMNAME', 'Aftaleindhold')
    afklaring_table.setCurrentCell(row_index, 'ID')
    afklaring_table.clickCurrentCell()
