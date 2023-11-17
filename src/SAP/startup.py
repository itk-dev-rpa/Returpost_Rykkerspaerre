from ITK_dev_shared_components.SAP import gridview_util

def open_afklaringsliste(session):
    session.findById("wnd[0]/tbar[0]/okcd").text = "emmacl"
    session.findById("wnd[0]").sendVKey(0)
    session.findById("wnd[0]/tbar[1]/btn[17]").press()
    session.findById("wnd[1]/usr/txtV-LOW").text = "standard"
    session.findById("wnd[1]/usr/txtENAME-LOW").text = ""
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/tbar[1]/btn[8]").press()

def select_layout(session, layout):
    session.findById("wnd[0]/tbar[1]/btn[33]").press()
    layout_table = session.findById("wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell")
    row_index = gridview_util.find_row_index_by_value(layout_table, "VARIANT", layout)
    layout_table.setCurrentCell(row_index, 'VARIANT')
    layout_table.clickCurrentCell()
    