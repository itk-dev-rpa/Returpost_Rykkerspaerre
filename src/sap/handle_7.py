"""This module handles all Rykkerspærre of type '7'."""

from datetime import date, timedelta

import pyodbc
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from itk_dev_shared_components.sap import gridview_util, opret_kundekontakt

from . import common


def handle_7(orchestrator_connection: OrchestratorConnection, session, fmcacov_session):
    """Go through the list of type '7' rykkerspærre and handle them."""
    fmcacov_session.StartTransaction('FMCACOV')

    case_table = session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell')
    gridview_util.scroll_entire_table(case_table, True)
    fp_list = get_fp_list(case_table)

    for fp in fp_list:
        orchestrator_connection.log_info(f"Rykkerspærre 7, begynder fp: {fp}")

        should_skip = not check_fp(fmcacov_session, fp)
        if should_skip:
            continue

        row_indices = gridview_util.find_all_row_indices_by_value(case_table, "ZZ_PARTNER", fp)

        extend_all_rykkerspaerrer_deadlines(session, row_indices)

        aftaler = collect_aftaler(session, row_indices)

        orchestrator_connection.log_info(f"Opretter kundekontakt på: FP: {fp}; Aftaler: {aftaler}")

        opret_kundekontakt.opret_kundekontakter(fmcacov_session, fp, aftaler, 'Orientering', 'Debitor har ikke fået digital post eller ny adresse. Henstand givet pga. manglende adresse. Der følges op på sagen om 3 måneder.')


def collect_aftaler(session, row_indices):
    """Collect all aftale ids in the given rows."""
    case_table = session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell')
    aftaler = []
    for row in row_indices:
        aftale = case_table.getCellValue(row, 'ZZPSOBKEY')
        aftaler.append(aftale)
    return aftaler


def extend_all_rykkerspaerrer_deadlines(session, row_indices):
    """Extend all deadlines on the rykkerspærrer on the given rows, assuming they have been handled."""
    case_table = session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell')
    for row in row_indices:
        common.open_aftaleindhold(session, case_table, row)

        # Check rykkerspærre type
        type = session.findById("wnd[0]/usr/subBDT_AREA:SAPLBUSS:0021/tabsBDT_TABSTRIP01/tabpBUSCR02_01/ssubGENSUB:SAPLBUSS:0029/ssubGENSUB:SAPLBUSS:7135/subA04P02:SAPLFMCA_PSOB_BDT2:0330/ctxtSPSOB_SCR_2110_H3-DUNN_REASON").text
        if type and type != '7':
            raise ValueError(f"Rykkerspæretype is not '7': '{type}'")

        # Edit date
        new_date = (date.today() + timedelta(days=90)).strftime("%d.%m.%Y")
        session.findById("wnd[0]/usr/btnPUSHB_CHANGE").press()
        session.findById("wnd[0]/usr/subBDT_AREA:SAPLBUSS:0021/tabsBDT_TABSTRIP01/tabpBUSCR02_01/ssubGENSUB:SAPLBUSS:0029/ssubGENSUB:SAPLBUSS:7135/subA04P03:SAPLZDKD0001_CUSTOM_SCREENS:0510/ctxtGV_DUNN_TDATE_CO").text = new_date
        session.findById("wnd[0]/tbar[0]/btn[11]").press()

        # Set status to 'Afsluttet and save
        session.findById("wnd[0]/usr/cmbEMMAD_CASEHDR-STATUS").value = "Afsluttet"
        session.findById("wnd[0]/tbar[0]/btn[11]").press()


def get_fp_list(case_table):
    """Get all unique fp-numbers from the table.
    Exclude ones that has a value in the bilagsnummer column.
    """
    fp_set = set()
    for row in range(case_table.RowCount):
        fp = case_table.getCellValue(row, 'ZZ_PARTNER')
        fp_set.add(fp)

    # Remove any that has a value in the bilagsnummer column
    for row in range(case_table.RowCount):
        bilag = case_table.getCellValue(row, 'ZZOPBEL')
        if bilag:
            fp = case_table.getCellValue(row, 'ZZ_PARTNER')
            if fp in fp_set:
                fp_set.remove(fp)

    return tuple(fp_set)


def check_fp(session, fp_number):
    """Check if fp should be handled. Returns false if the fp should be skipped"""
    # Search fp
    session.findById("wnd[0]/usr/ctxtGPART_DYN").text = fp_number
    session.findById("wnd[0]").sendVKey(0)

    # Refresh
    session.findById("wnd[0]/usr/btnZDKD_DP_REFRESH").press()
    popup = session.findById('wnd[1]/tbar[0]/btn[0]', False)
    if popup:
        popup.press()
        return False

    # Read Digital Post status
    dp_status = session.findById('wnd[0]/usr/txtZDKD_DIGITAL_POST').text
    if dp_status not in ('Ukendt', 'Fritaget'):
        return False

    cpr = session.findById('wnd[0]/usr/txtZDKD_BP_NUM').text
    cpr = cpr.replace('-', '')
    is_address_old = check_address_date(cpr)
    return is_address_old


def check_address_date(cpr: str):
    """Return true if the cpr has an aktuel_adresse that is more than 3 months old"""
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=FaellesSQL;Trusted_Connection=yes;")
    cursor = conn.execute(f"SELECT DatoFra FROM DWH.Mart.AdresseAktuel WHERE CPR = '{cpr}'")
    if cursor.rowcount == 0:
        return False

    # Check if date is older than 3 months
    date_from = cursor.fetchone()[0]
    if date_from is not None and date_from < (date.today() - timedelta(days=90)):
        return True

    return False
