import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# Define the structure for MIB files and their fields
mib_description = {
    'tcp.dat': {
        'TCP_ID': ['char', 8, 'M'],    # Field: [Type, Length, Applicability]
        'TCP_DESC': ['char', 24, 'O'],  # Field: [Type, Length, Applicability]
    },
    'pcpc.dat': { 
        'PCPC_PNAME': ['char', 8, 'M'],
        'PCPC_DESC': ['char', 24, 'M'],
        'PCPC_CODE': ['char', 1, 'O'],
    },
    'pcdf.dat': {
        'PCDF_TCNAME': ['char', 8, 'M'],
        'PCDF_DESC': ['char', 24, 'O'],
        'PCDF_TYPE': ['char', 1, 'M', ['F', 'A', 'T', 'S', 'K', 'P']],
        'PCDF_NAME': ['number', 4, 'M'],
        'PCDF_BIT': ['number', 4, 'M'],
        'PCDF_PNAME': ['char', 8, 'O'],
        'PCDF_VALUE': ['char', 10, 'M'],
        'PCDF_RADIX': ['char', 1, 'O', ['D', 'H', 'O']],
    },
    'ccf.dat': {
        'CCF_CNAME': ['char', 8, 'M'],
        'CCF_DESCR': ['char', 24, 'M'],
        'CCF_DESCR2': ['char', 64, 'O'],
        'CCF_CTYPE': ['char', 8, 'O', ['R', 'F', 'S', 'T', 'N']],
        'CCF_CRITICAL': ['char', 1, 'O', ['Y', 'N']],
        'CCF_PKTID': ['char', 8, 'M'],
        'CCF_TYPE': ['number', 3, 'O'],
        'CCF_STYPE': ['number', 3, 'O'],
        'CCF_APID': ['number', 5, 'O'],
        'CCF_NPARS': ['number', 3, 'O'],
        'CCF_PLAN': ['char', 1, 'O', ['A', 'F', 'S', 'N']],
        'CCF_EXEC': ['char', 1, 'O', ['Y', 'N']],
        'CCF_ILSCOPE': ['char', 1, 'O', ['G', 'L', 'S', 'B', 'F', 'T', 'N']],
        'CCF_ILSTAGE': ['char', 1, 'O', ['R', 'U', 'O', 'A', 'C']],
        'CCF_SUBSYS': ['number', 3, 'O'],
        'CCF_HIPRI': ['char', 1, 'O', ['Y', 'N']],
        'CCF_MAPID': ['number', 2, 'O'],
        'CCF_DEFSET': ['char', 8, 'O'],
        'CCF_RAPID': ['number', 5, 'O'],
        'CCF_ACK': ['number', 2, 'O'],
        'CCF_SUBSCHEDID': ['number', 5, 'O'],
    },
    'dst.dat': {  # Newly added file
        'DST_APID': ['number', 5, 'M'],
        'DST_ROUTE': ['char', 30, 'M'],
    },
    'vdf.dat': {  # Newly added file
        'VDF_NAME': ['char', 8, 'M'],
        'VDF_COMMENT': ['char', 32, 'O'],
        'VDF_DOMAIND': ['number', 5, 'O'],
        'VDF_RELEASE': ['number', 5, 'O'],
        'VDF_ISSUE': ['number', 5, 'O'],
    },
    'cpc.dat': {  # Newly added file
        'CPC_PNAME': ['char', 8, 'M'],
        'CPC_DESCR': ['char', 24, 'O'],
        'CPC_PTC': ['number', 2, 'M'],
        'CPC_PFC': ['number', 5, 'M'],
        'CPC_DISPFMT': ['char', 1, 'O', ['A', 'I', 'U', 'R', 'T', 'D']],
        'CPC_RADIX': ['char', 1, 'O', ['D', 'H', 'O']],
        'CPC_UNIT': ['char', 4, 'O'],
        'CPC_CATEG': ['char', 1, 'O', ['C', 'T', 'B', 'A', 'P', 'N']],
        'CPC_PRFREF': ['char', 10, 'O'],
        'CPC_CCAREF': ['char', 10, 'O'],
        'CPC_PAFREF': ['char', 10, 'O'],
        'CPC_INTER': ['char', 1, 'O', ['R', 'E']],
        'CPC_DEFVAL': ['char', 248, 'O'], #maximum allowed is taken as 248
        'CPC_CORR': ['char', 1, 'O', ['Y', 'N']],
        'CPC_OBTID': ['number', 5, 'O'],
        'CPC_DESCR2': ['char', 256, 'O'],
    },
    'pic.dat': {  # Newly added file
        'PIC_TYPE': ['number', 3, 'M'],
        'PIC_STYPE': ['number', 3, 'M'],
        'PIC_PI1_OFF': ['number', 5, 'M'],
        'PIC_PI1_WID': ['number', 3, 'M'],
        'PIC_PI2_OFF': ['number', 5, 'M'],
        'PIC_PI2_WID': ['number', 3, 'M'],
        'PIC_APID': ['number', 5, 'O'],
    },
    'plf.dat': {  # Newly added file
        'PLF_NAME': ['char', 8, 'M'],
        'PLF_SPID': ['number', 10, 'M'],
        'PLF_OFFBY': ['number', 5, 'M'],
        'PLF_OFFBI': ['number', 1, 'M'],
        'PLF_NBOCC': ['number', 4, 'O'],
        'PLF_LGOCC': ['number', 5, 'O'],
        'PLF_TIME': ['number', 9, 'O'],
        'PLF_TDOCC': ['number', 9, 'O'],
    },
    'vpd.dat': {  # Newly added file
        'VPD_TPSD': ['number', 10, 'M'],
        'VPD_POS': ['number', 4, 'M'],
        'VPD_NAME': ['char', 8, 'M'],
        'VPD_GRPSIZE': ['number', 3, 'O'],
        'VPD_FIXREP': ['number', 3, 'O'],
        'VPD_CHOICE': ['char', 1, 'O'],
        'VPD_PIDREF': ['char', 1, 'O'],
        'VPD_DISDESC': ['char', 16, 'O'],
        'VPD_WIDTH': ['numbwe', 2, 'M'],
        'VPD_JUSTIFY': ['char', 1, 'O'],
        'VPD_NEWLINE': ['char', 1, 'O'],
        'VPD_DCHAR': ['number', 1, 'O'],
        'VPD_FORM': ['char', 1, 'O'],
        'VPD_OFFSET': ['number', 6, 'O'],
    },
    'grp.dat': {  # Newly added file
        'GRP_NAME': ['char', 14, 'M'],
        'GRP_DESCR': ['char', 24, 'M'],
        'GRP_GTYPE': ['char', 2, 'M'],
    },
    'grpa.dat': {  # Newly added file
        'GRPA_GNAME': ['char', 14, 'M'],
        'GRPA_PANAME': ['char', 8, 'M'],
    },
    'grpk.dat': {  # Newly added file
        'GRPK_GNAME': ['char', 14, 'M'],
        'GRPK_PKSPID': ['char', 10, 'M'],
    },
    'dpf.dat': {  # Newly added file
        'DPF_NUMBE': ['char', 8, 'M'],
        'DPF_TYPE': ['char', 1, 'M'],
        'DPF_HEAD': ['char', 32, 'O'],
    },
    'dpc.dat': {  # Newly added file
        'DPC_NUMBE': ['char', 8, 'M'],
        'DPC_NAME': ['char', 8, 'O'],
        'DPC_FLDN': ['number', 2, 'M'],
        'DPC_COMM': ['number', 4, 'O'],
        'DPC_MODE': ['char', 1, 'O'],
        'DPC_FORM': ['char', 1, 'O'],
        'DPC_TEXT': ['char', 32, 'O'],
    },
    'gpf.dat': {
        'GPF_NUMBE': ['char', 8, 'M'],
        'GPF_TYPE': ['char', 1, 'M'],
        'GPF_HEAD': ['char', 32, 'O'],
        'GPF_SCROL': ['char', 1, 'O'],
        'GPF_HCOPY': ['char', 1, 'O'],
        'GPF_DAYS': ['number', 2, 'M'],
        'GPF_HOURS': ['number', 2, 'M'],
        'GPF_MINUT': ['number', 2, 'M'],
        'GPF_AXCLR': ['char', 1, 'M'],
        'GPF_XTICK': ['number', 2, 'M'],
        'GPF_YTICK': ['number', 2, 'M'],
        'GPF_XGRID': ['number', 2, 'M'],
        'GPF_YGRID': ['number', 2, 'M'],
        'GPF_UPUN': ['number', 2, 'O']
    },

    'gpc.dat': {
        'GPC_NUMBE': ['char', 8, 'M'],
        'GPC_POS': ['number', 1, 'M'],
        'GPC_WHERE': ['char', 1, 'M'],
        'GPC_NAME': ['char', 8, 'M'],
        'GPC_SYMB0': ['char', 1, 'O'],
        'GPC_LINE': ['char', 1, 'O'],
        'GPC_DOMAIN': ['number', 5, 'O']
    },

    'spf.dat': {
        'SPF_NUMBE': ['char', 8, 'M'],
        'SPF_HEAD': ['char', 32, 'O'],
        'SPF_NPAR': ['number', 1, 'M'],
        'SPF_UPUN': ['number', 2, 'O']
    },

    'spc.dat': {
        'SPC_NUMBE': ['char', 8, 'M'],
        'SPC_POS': ['number', 1, 'M'],
        'SPC_NAME': ['char', 8, 'M'],
        'SPC_UPDT': ['char', 1, 'O'],
        'SPC_MODE': ['char', 1, 'O'],
        'SPC_FORM': ['char', 1, 'O'],
        'SPC_BACK': ['char', 1, 'O'],
        'SPC_FORE': ['char', 1, 'M']
    },
    'cdf.dat': {  # Newly added file
        'CDF_CNAME': ['char', 8, 'M'],
        'CDF_ELTYPE': ['char', 1, 'M'],
        'CDF_DESCR': ['char', 24, 'O'],
        'CDF_ELLEN': ['number', 4, 'M'],
        'CDF_BIT': ['number', 4, 'M'],
        'CDF_GRPSIZE': ['number', 2, 'O'],
        'CDF_PNAME': ['char', 8, 'O'],
        'CDF_INTER': ['char', 1, 'O'],
        'CDF_VALUE': ['char', 248, 'O'], #maximum allowed is taken as 248
        'CDF_TMID': ['char', 8, 'O'],
    },
    'ptv.dat': {  # Newly added file
        'PTV_CNAME': ['char', 8, 'M'],
        'PTV_PARNAM': ['char', 8, 'M'],
        'PTV_INTER': ['char', 1, 'O'],
        'PTV_VAL': ['char', 17, 'M'],
    },
    'csf.dat': {  # Newly added file
        'CSF_NAME': ['char', 8, 'M'],
        'CSF_DESC': ['char', 24, 'M'],
        'CSF_DESC2': ['char', 64, 'O'],
        'CSF_IFTT': ['char', 1, 'O'],
        'CSF_NFPARS': ['number', 3, 'O'],
        'CSF_ELEMS': ['number', 5, 'O'],
        'CSF_CRITICAL': ['char', 1, 'O'],
        'CSF_PLAN': ['char', 1, 'O'],
        'CSF_EXEC': ['char', 1, 'O'],
        'CSF_SUBSYS': ['number', 3, 'O'],
        'CSF_GENTIME': ['char', 17, 'O'],
        'CSF_DOCNAME': ['char', 32, 'O'],
        'CSF_ISSUE': ['char', 10, 'O'],
        'CSF_DATE': ['char', 17, 'O'],
        'CSF_DEFSET': ['char', 8, 'O'],
        'CSF_SUBSCHEDID': ['number', 5, 'O'],
    },
    'css.dat': {
        'CSS_SQNAME': ['char', 8, 'M'],
        'CSS_COMM': ['char', 32, 'O'],
        'CSS_ENTRY': ['number', 5, 'M'],
        'CSS_TYPE': ['char', 1, 'M'],
        'CSS_ELEMID': ['char', 8, 'O'],
        'CSS_NPARS': ['number', 3, 'O'],
        'CSS_MANDISP': ['char', 1, 'O'],
        'CSS_RELTYPE': ['char', 1, 'O'],
        'CSS_RELTIME': ['char', 12, 'O'],
        'CSS_EXTIME': ['char', 17, 'O'],
        'CSS_PREVREL': ['char', 1, 'O'],
        'CSS_GROUP': ['char', 1, 'O'],
        'CSS_BLOCK': ['char', 1, 'O'],
        'CSS_ILSTAGE': ['char', 1, 'O'],
        'CSS_DYNPTV': ['char', 1, 'O'],
        'CSS_STAPTV': ['char', 1, 'O'],
        'CSS_CEV': ['char', 1, 'O'],
        'CSS_SUBSYS': ['number', 3, 'O']
    }, 
    'sdf.dat': {
        'SDF_SQNAME': ['char', 8, 'M'],
        'SDF_ENTRY': ['number', 5, 'M'],
        'SDF_ELEMID': ['char', 8, 'M'],
        'SDF_POS': ['number', 4, 'M'],
        'SDF_PNAME': ['char', 8, 'M'],
        'SDF_FTYPE': ['char', 1, 'O'],
        'SDF_VTYPE': ['char', 1, 'O'],
        'SDF_VALUE': ['char', 248, 'O'],  # Max size depends on command limits.
        'SDF_VALSET': ['char', 8, 'O'],
        'SDF_REPPOS': ['number', 4, 'O'],
    },
    'csp.dat': {
        'CSP_SQNAME': ['char', 8, 'M'],
        'CSP_FPNAME': ['char', 8, 'M'],
        'CSP_FPNUM': ['number', 5, 'M'],
        'CSP_DESCR': ['char', 24, 'O'],
        'CSP_PTC': ['number', 2, 'M'],
        'CSP_PFC': ['number', 5, 'M'],
        'CSP_DISPFMT': ['char', 1, 'O'],
        'CSP_RADIX': ['char', 1, 'O'],
        'CSP_TYPE': ['char', 1, 'M'],
        'CSP_VTYPE': ['char', 1, 'O'],
        'CSP_DEFVAL': ['char', 248, 'O'],  # Max size depends on parameter type limits.
        'CSP_CATEG': ['char', 1, 'O'],
        'CSP_PRFREF': ['char', 10, 'O'],
        'CSP_CCAREF': ['char', 10, 'O'],
        'CSP_PAFREF': ['char', 10, 'O'],
        'CSP_UNIT': ['char', 4, 'O'],
    },
    'cvs.dat': {
        'CVS_ID': ['number', 5, 'M'],
        'CVS_TYPE': ['char', 1, 'M'],
        'CVS_SOURCE': ['char', 1, 'M'],
        'CVS_START': ['number', 5, 'M'],
        'CVS_INTERVAL': ['number', 5, 'M'],
        'CVS_SPID': ['number', 10, 'O']
    },
    'cve.dat': {
        'CVE_CVSID': ['number', 5, 'M'],
        'CVE_PARNAM': ['char', 8, 'M'],
        'CVE_INTER': ['char', 1, 'M'],
        'CVE_VAL': ['char', 17, 'O'],
        'CVE_TOL': ['char', 17, 'O'],
        'CVE_CHECK': ['char', 1, 'O']
    },
    'cvp.dat': {
        'CVP_TASK': ['char', 8, 'M'],
        'CVP_TYPE': ['char', 1, 'M'],
        'CVP_CVSID': ['number', 5, 'M']
    },
    'pst.dat': {
        'PST_NAME': ['char', 8, 'M'],
        'PST_DESCR': ['char', 24, 'O']
    },
    'psv.dat': {
        'PSV_NAME': ['char', 8, 'M'],
        'PSV_PVSID': ['char', 8, 'M'],
        'PSV_DESCR': ['char', 24, 'O']
    },
    'cps.dat': {
        'CPS_NAME': ['char', 8, 'M'],
        'CPS_PAR': ['char', 8, 'M'],
        'CPS_BIT': ['number', 4, 'M']
    },
    'pvs.dat': {
        'PVS_ID': ['char', 8, 'M'],
        'PVS_PSID': ['char', 8, 'M'],
        'PVS_PNAME': ['char', 8, 'M'],
        'PVS_INTER': ['char', 1, 'O'],
        'PVS_VALS': ['char', 248, 'O'],  # Max size depends on the command
        'PVS_BIT': ['number', 4, 'M']
    },
    'psm.dat': {
        'PSM_NAME': ['char', 8, 'M'],
        'PSM_TYPE': ['char', 1, 'M'],
        'PSM_PARSET': ['char', 8, 'M']
    },
    'cca.dat': {
        'CCA_NUMBR': ['char', 10, 'M'],
        'CCA_DESCR': ['char', 32, 'O'],
        'CCA_ENGFMT': ['char', 1, 'M'],
        'CCA_RAWFMT': ['char', 1, 'M'],
        'CCA_RADIX': ['char', 1, 'O'],
        'CCA_UNIT': ['char', 4, 'O']
    },
    'ccs.dat': {
        'CCS_NUMBR': ['char', 10, 'M'],
        'CCS_RAW': ['char', 14, 'M'],
        'CCS_ENG': ['char', 14, 'M']
    },
    'paf.dat': {
        'PAF_NUMBR': ['char', 10, 'M'],
        'PAF_DESCR': ['char', 32, 'O'],
        'PAF_RAWFMT': ['char', 1, 'M']
    },
    'pas.dat': {
        'PAS_NUMBR': ['char', 10, 'M'],
        'PAS_ALTXT': ['char', 248, 'M'],
        'PAS_ALVAL': ['char', 248, 'M']
    },
    'prf.dat': {
        'PRF_NUMBR': ['char', 10, 'M'],
        'PRF_DESCR': ['char', 24, 'O'],
        'PRF_INTER': ['char', 1, 'O']
    },
    'prv.dat': {
        'PRV_NUMBR': ['char', 10, 'M'],
        'PRV_MINVAL': ['char', 14, 'O'],
        'PRV_MAXVAL': ['char', 14, 'O']
    },
    'pcf.dat': {
        'PCF_NAME': ['char', 8, 'M'],
        'PCF_DESCR': ['char', 24, 'O'],
        'PCF_PID': ['number', 10, 'O'],
        'PCF_UNIT': ['char', 4, 'O'],
        'PCF_PTC': ['number', 2, 'M'],
        'PCF_PFC': ['number', 5, 'M'],
        'PCF_WIDTH': ['number', 6, 'O'],
        'PCF_VALID': ['char', 8, 'O'],
        'PCF_RELATED': ['char', 8, 'O'],
        'PCF_CATEG': ['char', 1, 'M'],
        'PCF_NATUR': ['char', 1, 'M'],
        'PCF_CURTX': ['char', 10, 'O'],
        'PCF_INTER': ['char', 1, 'O'],
        'PCF_USCON': ['char', 1, 'O'],
        'PCF_DECIM': ['number', 3, 'O'],
        'PCF_PARVAL': ['char', 14, 'O'],
        'PCF_SUBSYS': ['char', 8, 'O'],
        'PCF_VALPAR': ['number', 5, 'O'],
        'PCF_SPTYPE': ['char', 1, 'O'],
        'PCF_CORR': ['char', 1, 'O'],
        'PCF_OBTID': ['number', 5, 'O'],
        'PCF_DARC': ['char', 1, 'O'],
        'PCF_ENDIAN': ['char', 1, 'O'],
        'PCF_DESCR2': ['char', 256, 'O'],
    },
    'cur.dat': {
        'CUR_PNAME': ['char', 8, 'M'],
        'CUR_POS': ['number', 2, 'M'],
        'CUR_RLCHK': ['char', 8, 'M'],
        'CUR_VALPAR': ['number', 5, 'M'],
        'CUR_SELECT': ['char', 10, 'M']
    },
    'caf.dat': {
        'CAF_NUMBR': ['char', 10, 'M'],
        'CAF_DESCR': ['char', 32, 'O'],
        'CAF_ENGFMT': ['char', 1, 'M'],
        'CAF_RAWFMT': ['char', 1, 'M'],
        'CAF_RADIX': ['char', 1, 'O'],
        'CAF_UNIT': ['char', 4, 'O'],
        'CAF_NCURVE': ['number', 3, 'O'],
        'CAF_INTER': ['char', 1, 'O']
    },
    'cap.dat': {
        'CAP_NUMBR': ['char', 10, 'M'],
        'CAP_XVALS': ['char', 14, 'M'],
        'CAP_YVALS': ['char', 14, 'M']
    },       
    'txf.dat': {
        'TXF_NUMBR': ['char', 10, 'M'],
        'TXF_DESCR': ['char', 32, 'O'],
        'TXF_RAWFMT': ['char', 1, 'M'],
        'TXF_NALIAS': ['number', 3, 'O']
    },
    'txp.dat': {
        'TXP_NUMBR': ['char', 10, 'M'],
        'TXP_FROM': ['char', 14, 'M'],
        'TXP_TO': ['char', 14, 'M'],
        'TXP_ALTXT': ['char', 14, 'M']
    },
    'mcf.dat': {
        'MCF_IDENT': ['char', 10, 'M'],
        'MCF_DESCR': ['char', 32, 'O'],
        'MCF_POL1': ['char', 14, 'M'],
        'MCF_POL2': ['char', 14, 'O'],
        'MCF_POL3': ['char', 14, 'O'],
        'MCF_POL4': ['char', 14, 'O'],
        'MCF_POL5': ['char', 14, 'O']
    },
    'lgf.dat': {
        'LGF_IDENT': ['char', 10, 'M'],
        'LGF_DESCR': ['char', 32, 'O'],
        'LGF_POL1': ['char', 14, 'M'],
        'LGF_POL2': ['char', 14, 'O'],
        'LGF_POL3': ['char', 14, 'O'],
        'LGF_POL4': ['char', 14, 'O'],
        'LGF_POL5': ['char', 14, 'O']
    },
    'ocf.dat': {
        'OCF_NAME': ['char', 8, 'M'],
        'OCF_NBCHCK': ['number', 2, 'M'],
        'OCF_NBOOL': ['number', 2, 'M'],
        'OCF_INTER': ['char', 1, 'M'],
        'OCF_CODIN': ['char', 1, 'M']
    },
    'ocp.dat': {
        'OCP_NAME': ['char', 8, 'M'],
        'OCP_POS': ['number', 2, 'M'],
        'OCP_TYPE': ['char', 1, 'M'],
        'OCP_LVALU': ['char', 14, 'O'],
        'OCP_HVALU': ['char', 14, 'O'],
        'OCP_RLCHK': ['char', 8, 'O'],
        'OCP_VALPAR': ['number', 5, 'O']
    },
    'pid.dat': {
        'PID_TYPE': ['number', 3, 'M'],
        'PID_STYPE': ['number', 3, 'M'],
        'PID_APID': ['number', 5, 'M'],
        'PID_PI1_VAL': ['number', 10, 'O'],
        'PID_PI2_VAL': ['number', 10, 'O'],
        'PID_SPID': ['number', 10, 'M'],
        'PID_DESCR': ['char', 64, 'O'],
        'PID_UNIT': ['char', 8, 'O']
    },
    'pic.dat': {
        'PIC_TYPE': ['number', 3, 'M'],
        'PIC_STYPE': ['number', 3, 'M'],
        'PIC_PI1_OFF': ['number', 5, 'M'],
        'PIC_PI1_WID': ['number', 3, 'M'],
        'PIC_PI2_OFF': ['number', 5, 'M'],
        'PIC_PI2_WID': ['number', 3, 'M'],
        'PIC_APID': ['number', 5, 'O']
    },
    'tpcf.dat': {
        'TPCF_SPID': ['number', 10, 'M'],
        'TPCF_NAME': ['char', 12, 'O'],
        'TPCF_SIZE': ['number', 8, 'O']
    }
}

class MIBVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SCOS-2000 MIB Verifier")

        # Allow the window to be resizable
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.create_widgets()

        self.total_lines = 0
        self.total_checks = 0
        self.total_successful_checks = 0
        self.total_failed_checks = 0
        self.total_skipped_checks = 0  # For skipped optional and missing checks
        self.failed_check_details = []  # To track all failed checks
        self.unique_pname_check = set()  # For uniqueness check of PCPC_PNAME

    def create_widgets(self):
        # Select Folder Button
        self.select_button = tk.Button(self.root, text="Select MIB Folder", command=self.select_folder)
        self.select_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Text Box for displaying processed file names and warnings
        self.text_box = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.text_box.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Configure tags for different text styles
        self.text_box.tag_config('success', foreground='green')
        self.text_box.tag_config('failure', foreground='red')
        self.text_box.tag_config('warning', foreground='orange')
        self.text_box.tag_config('info', foreground='blue')
        self.text_box.tag_config('header', foreground='purple', font=('Helvetica', 12, 'bold'))

    def insert_text(self, text, tag=None):
        """Helper function to insert text into the text box with a specific tag."""
        self.text_box.insert(tk.END, text + "\n", tag)
        self.text_box.see(tk.END)  # Automatically scroll to the end

    def select_folder(self):
        # Reset the text box and counters
        self.text_box.delete(1.0, tk.END)  # Clear the text box before displaying new files
        self.reset_summary_counters()  # Reset summary counters
        
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.insert_text(f"Selected folder: {folder_selected}", 'info')
            self.process_dat_files(folder_selected)
            self.display_overall_summary()

    def reset_summary_counters(self):
        """Helper function to reset overall summary counters."""
        self.total_lines = 0
        self.total_checks = 0
        self.total_successful_checks = 0
        self.total_failed_checks = 0
        self.total_skipped_checks = 0
        self.failed_check_details = []  # Reset the failed check details list
        self.unique_pname_check = set()  # Reset unique PCPC_PNAME check
        
    def process_dat_files(self, folder):
        # Iterate through all files in the folder
        dat_files_found = False
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath) and filepath.lower().endswith('.dat'):
                # Check if the filename is in mib_description
                if filename in mib_description:
                    self.insert_text(f"Processing file: {filename}", 'info')
                    self.verify_file(filepath, filename)
                    dat_files_found = True
                else:
                    self.insert_text(f"Skipped unrecognized .dat file: {filename}", 'warning')

        if not dat_files_found:
            self.insert_text("No .dat files found in the selected folder.", 'warning')

    def verify_file(self, filepath, file_type):
        """Verifies the .dat file based on the mib_description structure"""
        self.insert_text(f"\nVerifying {os.path.basename(filepath)}...", 'header')

        description = mib_description.get(file_type)

        line_number = 0
        total_checks = 0
        successful_checks = 0
        failed_checks = 0
        skipped_checks = 0  # Skipped optional fields
        failed_check_details = []  # To track failed checks for this file

        unique_pcpc_pnames = set()  # To store unique PCPC_PNAMES values
        unique_pcf_names = set()  # To store unique PCF_NAME values
        unique_caf_numbr = set()  # To store unique CAF_NUMBR values
        unique_txf_numbr = set()  # To store unique TXF_NUMBR values
        unique_mcf_ident = set()  # To store unique MCF_IDENT values
        unique_lgf_ident = set()  # To store unique LGF_IDENT values
        unique_pid_spid = set()  # To store unique PID_SPID values
        unique_grp_name = set()  # To store unique GRP_NAME values
        unique_dpf_numbe = set()  # To store unique DPF_NUMBE values
        unique_gpf_numbe = set()  # To store unique GPF_NUMBE values
        unique_spf_numbe = set()  # To store unique SPF_NUMBE values
        unique_ppf_numbe = set()  # To store unique PPF_NUMBE values
        unique_tcp_id = set()  # To store unique TCP_ID values
        unique_ccf_cname = set()  # To store unique CCF_CNAME values
        unique_cpc_pname = set()  # To store unique CPC_PNAME values
        unique_csp_fpnum = set()  # To store unique CSP_FPNUM values
        unique_cvs_id = set()  # To store unique CVS_ID values
        unique_pst_name = set()  # To store unique PST_NAME values
        unique_psv_pvsid = set()  # To store unique PSV_PVSID values
        unique_cca_numbr = set()  # To store unique CCA_NUMBR values
        unique_paf_numbr = set()  # To store unique PAF_NUMBR values
        unique_prf_numbr = set()  # To store unique PRF_NUMBR values

        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line_number += 1
                    line = line.strip()
                    if not line:
                        continue

                    fields = line.split('\t')  # Assuming fields are separated by tab

                    def check_uniqueness(file_type, field_name, field_index, fields, unique_names, line_number, failed_checks, failed_check_details):
                        if field_index < len(fields):
                            pname_value = fields[field_index]
                            if pname_value in unique_names:
                                failed_checks += 1
                                failed_check_details.append(f"Line {line_number}: Duplicate {field_name} '{pname_value}' found.")
                            else:
                                unique_names.add(pname_value)
                        else:
                            failed_checks += 1
                            failed_check_details.append(f"Line {line_number}: {field_name} is missing.")
                        return failed_checks

                    def check_mandatory_field(field_index, fields, applicability, field_name, line_number, failed_checks, skipped_checks, failed_check_details):
                        if field_index >= len(fields):
                            if applicability == 'M':
                                failed_checks += 1
                                failed_check_details.append(f"Line {line_number}: {field_name} is mandatory but missing.")
                            else:
                                skipped_checks += 1
                        return failed_checks, skipped_checks

                    def validate_field_type_and_length(field_type, field_value, field_length, field_name, line_number, failed_checks, failed_check_details):
                        if field_type == 'char' and not isinstance(field_value, str):
                            failed_checks += 1
                            failed_check_details.append(f"Line {line_number}: {field_name} is expected to be a char.")
                        elif field_type == 'number':
                            try:
                                num_value = float(field_value)
                                if len(field_value.replace('-', '').replace('.', '')) > field_length:
                                    failed_checks += 1
                                    failed_check_details.append(f"Line {line_number}: {field_name} exceeds the length limit of {field_length} digits.")
                            except ValueError:
                                failed_checks += 1
                                failed_check_details.append(f"Line {line_number}: {field_name} is expected to be a number.")
                        return failed_checks

                    def validate_allowed_values(field_value, allowed_values, field_name, line_number, failed_checks, failed_check_details):
                        if allowed_values and field_value not in allowed_values:
                            failed_checks += 1
                            failed_check_details.append(f"Line {line_number}: {field_name} has an invalid value '{field_value}'. Allowed values are: {', '.join(allowed_values)}.")
                        return failed_checks

                    def check_mandatory_value(field_value, applicability, field_name, line_number, failed_checks, failed_check_details):
                        if applicability == 'M' and not field_value:
                            failed_checks += 1
                            failed_check_details.append(f"Line {line_number}: {field_name} is mandatory but missing or undefined.")
                        return failed_checks

                    # Main loop refactored
                    for field_name, field_properties in description.items():
                        field_type = field_properties[0]
                        field_length = field_properties[1]
                        applicability = field_properties[2]
                        allowed_values = field_properties[3] if len(field_properties) > 3 else None
                        field_index = list(description.keys()).index(field_name)
                        total_checks += 1

                        # Special uniqueness checks
                        if file_type == 'pcpc.dat' and field_name == 'PCPC_PNAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_pcpc_pnames, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'pcf.dat' and field_name == 'PCF_NAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_pcf_names, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'caf.dat' and field_name == 'CAF_NUMBR':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_caf_numbr, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'txf.dat' and field_name == 'TXF_NUMBR':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_txf_numbr, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'mcf.dat' and field_name == 'MCF_IDENT':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_mcf_ident, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'lgf.dat' and field_name == 'LGF_IDENT':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_lgf_ident, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'pid.dat' and field_name == 'PID_SPID':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_pid_spid, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'grp.dat' and field_name == 'GRP_NAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_grp_name, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'dpf.dat' and field_name == 'DPF_NUMBE':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_dpf_numbe, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'gpf.dat' and field_name == 'GPF_NUMBE':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_gpf_numbe, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'spf.dat' and field_name == 'SPF_NUMBE':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_spf_numbe, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'ppf.dat' and field_name == 'PPF_NUMBE':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_ppf_numbe, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'tcp.dat' and field_name == 'TCP_ID':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_tcp_id, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'ccf.dat' and field_name == 'CCF_CNAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_ccf_cname, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'cpc.dat' and field_name == 'CPC_PNAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_cpc_pname, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'csp.dat' and field_name == 'CSP_FPNUM':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_csp_fpnum, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'cvs.dat' and field_name == 'CVS_ID':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_cvs_id, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'pst.dat' and field_name == 'PST_NAME':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_pst_name, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'psv.dat' and field_name == 'PSV_PVSID':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_psv_pvsid, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'cca.dat' and field_name == 'CCA_NUMBR':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_cca_numbr, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'paf.dat' and field_name == 'PAF_NUMBR':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_paf_numbr, line_number, failed_checks, failed_check_details)
                            continue
                        if file_type == 'prf.dat' and field_name == 'PRF_NUMBR':
                            failed_checks = check_uniqueness(file_type, field_name, field_index, fields, unique_prf_numbr, line_number, failed_checks, failed_check_details)
                            continue

                        # Mandatory field check
                        failed_checks, skipped_checks = check_mandatory_field(field_index, fields, applicability, field_name, line_number, failed_checks, skipped_checks, failed_check_details)
                        if field_index >= len(fields):
                            continue

                        field_value = fields[field_index]

                        # Field validation
                        if field_value:
                            failed_checks = validate_field_type_and_length(field_type, field_value, field_length, field_name, line_number, failed_checks, failed_check_details)
                            if failed_checks:
                                continue

                            failed_checks = validate_allowed_values(field_value, allowed_values, field_name, line_number, failed_checks, failed_check_details)
                            if failed_checks:
                                continue

                        # Mandatory value check
                        failed_checks = check_mandatory_value(field_value, applicability, field_name, line_number, failed_checks, failed_check_details)
                        if failed_checks:
                            continue

                        # If no issues, consider this a successful check
                        successful_checks += 1

            # Summary of the processing for this file
            self.insert_text(f"\nSummary of {os.path.basename(filepath)} verification:", 'header')
            self.insert_text(f"\tTotal lines processed: {line_number}", 'info')
            self.insert_text(f"\tTotal checks performed: {total_checks}", 'info')
            self.insert_text(f"\tSuccessful checks: {successful_checks}/{total_checks}", 'success')
            self.insert_text(f"\tFailed checks: {failed_checks}", 'failure')
            self.insert_text(f"\tSkipped optional checks: {skipped_checks}", 'info')

            # Report failed checks for this file
            if failed_checks > 0:
                self.insert_text("\nFailed checks for this file:", 'failure')
                for failure in failed_check_details:
                    self.insert_text(f"\t{failure}", 'failure')

            self.insert_text(f"Verification of {os.path.basename(filepath)} completed.", 'success')

            # Update overall summary stats
            self.total_lines += line_number
            self.total_checks += total_checks
            self.total_successful_checks += successful_checks
            self.total_failed_checks += failed_checks
            self.total_skipped_checks += skipped_checks

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading {filepath}: {e}")
            self.insert_text(f"Error reading {filepath}", 'failure')

    def display_overall_summary(self):
        """Displays an overall summary for all files processed."""
        self.insert_text("\n--- Overall Summary ---", 'header')
        self.insert_text(f"Total lines processed: {self.total_lines}", 'info')
        self.insert_text(f"Total checks performed: {self.total_checks}", 'info')
        self.insert_text(f"Total successful checks: {self.total_successful_checks}/{self.total_checks}", 'success')
        self.insert_text(f"Total failed checks: {self.total_failed_checks}", 'failure')
        self.insert_text(f"Total skipped optional checks: {self.total_skipped_checks}", 'info')

        self.insert_text("--- End of Summary ---", 'header')


# Add main function
def main():
    root = tk.Tk()
    app = MIBVerifierApp(root)
    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()
