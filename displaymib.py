import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Mapping file names to their corresponding headers
file_headers = {
    'vdf': ['VDF_NAME', 'VDF_COMMENT', 'VDF_DOMAINID', 'VDF_RELEASE', 'VDF_ISSUE'],
    'pcf': ['PCF_NAME', 'PCF_DESCR', 'PCF_PID', 'PCF_UNIT', 'PCF_PTC', 'PCF_PFC', 'PCF_WIDTH', 'PCF_VALID', 'PCF_RELATED', 'PCF_CATEG', 'PCF_NATUR', 'PCF_CURTX', 'PCF_INTER', 'PCF_USCON', 'PCF_DECIM', 'PCF_PARVAL', 'PCF_SUBSYS', 'PCF_VALPAR', 'PCF_SPTYPE', 'PCF_CORR', 'PCF_OBTID', 'PCF_DARC', 'PCF_ENDIAN', 'PCF_DESCR2'],
    'cur': ['CUR_PNAME', 'CUR_POS', 'CUR_RLCHK', 'CUR_VALPAR', 'CUR_SELECT'],
    'caf': ['CAF_NUMBR', 'CAF_DESCR', 'CAF_ENGFMT', 'CAF_RAWFMT', 'CAF_RADIX', 'CAF_UNIT', 'CAF_NCURVE', 'CAF_INTER'],
    'cap': ['CAP_NUMBR', 'CAP_XVALS', 'CAP_YVALS'],
    'txf': ['TXF_NUMBR', 'TXF_DESCR', 'TXF_RAWFMT', 'TXF_NALIAS'],
    'txp': ['TXP_NUMBR', 'TXP_FROM', 'TXP_TO', 'TXP_ALTXT'],
    'mcf': ['MCF_IDENT', 'MCF_DESCR', 'MCF_POL1', 'MCF_POL2', 'MCF_POL3', 'MCF_POL4', 'MCF_POL5'],
    'lgf': ['LGF_IDENT', 'LGF_DESCR', 'LGF_POL1', 'LGF_POL2', 'LGF_POL3', 'LGF_POL4', 'LGF_POL5'],
    'ocf': ['OCF_NAME', 'OCF_NBCHCK', 'OCF_NBOOL', 'OCF_INTER'],
    'ocp': ['OCP_NAME', 'OCP_POS', 'OCP_TYPE', 'OCP_LVALU', 'OCP_HVALU', 'OCP_RLCHK', 'OCP_VALPAR'],
    'pid': ['PID_TYPE', 'PID_STYPE', 'PID_APID', 'PID_PI1_VAL', 'PID_PI2_VAL', 'PID_SPID', 'PID_DESCR', 'PID_UNIT', 'PID_TPSD', 'PID_DFHSIZE', 'PID_TIME', 'PID_INTER', 'PID_VALID', 'PID_CHECK', 'PID_EVENT', 'PID_EVID'],
    'pic': ['PIC_TYPE', 'PIC_STYPE', 'PIC_PI1_OFF', 'PIC_PI1_WID' ,'PIC_PI2_OFF', 'PIC_PI2_WID', 'PIC_APID'],
    'tpcf': ['TPCF_SPID', 'TPCF_NAME', 'TPCF_SIZE'],
    'plf': ['PLF_NAME', 'PLF_SPID', 'PLF_OFFBY', 'PLF_OFFBI', 'PLF_NBOCC', 'PLF_LGOCC', 'PLF_TIME', 'PLF_TDOCC'],
    'vpd': ['VPD_TPSD', 'VPD_POS', 'VPD_NAME', 'VPD_GRPSIZE', 'VPD_FIXREP', 'VPD_CHOICE', 'VPD_PIDREF', 'VPD_DISDESC', 'VPD_WIDTH', 'VPD_JUSTIFY', 'VPD_NEWLINE', 'VPD_DCHAR', 'VPD_FORM', 'VPD_OFFSET' ],
    'grp': ['GRP_NAME', 'GRP_DESCR', 'GRP_GTYPE'],
    'grpa': ['GRPA_NAME', 'GRPA_PANAME'],
    'grpk': ['GRPK_GNAME', 'GRPK_PKSPID'],
    'dpf': ['DPF_NUMBE', 'DPF_TYPE', 'DPF_HEAD'],
    'dpc': ['DPC_NUMBE', 'DPC_NAME', 'DPC_FLDN', 'DPC_COMM', 'DPC_MODE', 'DPC_FORM', 'DPC_TEXT'],
    'gpf': ['GPF_NUMBE', 'GPF_TYPE', 'GPF_HEAD', 'GPF_SCROL', 'GPF_HCOPY', 'GPF_DAYS', 'GPF_HOURS', 'GPF_MINUT', 'GPF_AXCLR', 'GPF_XTICK', 'GPF_YTICK', 'GPF_XGRID', 'GPF_YGRID', 'GPF_UPUN'],
    'gpc': ['GPC_NUMBE', 'GPC_POS', 'GPC_WHERE', 'GPC_NAME', 'GPC_RAW', 'GPC_MINIM', 'GPC_MAXIM', 'GPC_PRCLR', 'GPC_SYMB0', 'GPC_LINE', 'GPC_DOMAIN'],
    'spf': ['SPF_NUMBE', 'SPF_HEAD', 'SPF_NPAR', 'SPF_UPUN'],
    'spc': ['SPC_NUMBE', 'SPC_POS', 'SPC_NAME', 'SPC_UPDT', 'SPC_MODE', 'SPC_FORM', 'SPC_BACK', 'SPC_FORE'],
    'ppf': ['PPF_NUMBE', 'PPF_HEAD', 'PPF_NBPR'],
    'ppc': ['PPC_NUMBE', 'PPC_POS', 'PPC_NAME', 'PPC_FORM'],
    'tcp': ['TCP_ID', 'TCP_DESC'],
    'pcpc': ['PCPC_PNAME', 'PCPC_DESC', 'PCPC_CODE'],
    'pcdf': ['PCDF_TCNAME', 'PCDF_DESC', 'PCDF_TYPE', 'PCDF_LEN', 'PCDF_BIT', 'PCDF_PNAME', 'PCDF_VALUE', 'PCDF_RADIX'],
    'ccf': ['CCF_NAME', 'CCF_DESCR', 'CCF_DESCR2', 'CCF_CTYPE', 'CCF_CRITICAL', 'CCF_PKTID', 'CCF_TYPE', 'CCF_STYPE', 'CCF_APID', 'CCF_NPARS', 'CCF_PLAN', 'CCF_EXEC', 'CCF_ILSCOPE', 'CCF_ILSTAGE', 'CCF_SUBSYS', 'CCF_HIPRI', 'CCF_MAPID', 'CCF_DEFSET', 'CCF_RAPID', 'CCF_ACK', 'CCF_SUBSCHEDID'],
    'dst': ['DST_APID', 'DST_ROUTE'],
    'cpc': ['CPC_PNAME', 'CPC_DESCR', 'CPC_PTC', 'CPC_PFC', 'CPC_DISPFMT', 'CPC_RADIX', 'CPC_UNIT', 'CPC_CATEG', 'CPC_PRFREF', 'CPC_CCAREF', 'CPC_PAFREF', 'CPC_INTER', 'CPC_DEFVAL', 'CPC_CORR', 'CPC_OBTID', 'CPC_DESCR2', 'CPC_ENDIAN'],
    'cdf': ['CDF_CNAME', 'CDF_ELTYPE', 'CDF_DESCR', 'CDF_ELLEN', 'CDF_BIT', 'CDF_GRPSIZE', 'CDF_PNAME', 'CDF_INTER', 'CDF_VALUE', 'CDF_TMID'],
    'ptv': ['PTV_CNAME', 'PTV_PARNAM', 'PTV_INTER', 'PTV_VAL'],
    'csf': ['CSF_NAME', 'CSF_DESC', 'CSF_DESC2', 'CSF_IFTT', 'CSF_NFPARS', 'CSF_ELEMS', 'CSF_CRITICAL', 'CSF_PLAN', 'CSF_EXEC', 'CSF_SUBSYS', 'CSF_GENTIME', 'CSF_DOCNAME', 'CSF_ISSUE', 'CSF_DATE', 'CSF_DEFSET', 'CSF_SUBSCHEDID'],
    'css': ['CSS_SQNAME', 'CSS_COMM', 'CSS_ENTRY', 'CSS_TYPE', 'CSS_ELEMID', 'CSS_NPARS', 'CSS_MANDISP', 'CSS_RELTYPE', 'CSS_RELTIME', 'CSS_EXTIME', 'CSS_PREVREL', 'CSS_GROUP', 'CSS_BLOCK', 'CSS_ILSCOPE', 'CSS_ILSTAGE', 'CSS_DYNPTV', 'CSS_STAPTV', 'CSS_CEV'],
    'sdf': ['SDF_SQNAME', 'SDF_ENTRY', 'SDF_ELEMID', 'SDF_POS', 'SDF_PNAME', 'SDF_FTYPE', 'SDF_VTYPE', 'SDF_VALUE', 'SDF_VALSET', 'SDF_REPPOS'],
    'csp': ['CSP_SQNAME', 'CSP_FPNAME', 'CSP_FPNUM', 'CSP_DESCR', 'CSP_PTC', 'CSP_PFC', 'CSP_DISPFMT', 'CSP_RADIX', 'CSP_TYPE', 'CSP_VTYPE', 'CSP_DEFVAL', 'CSP_CATEG', 'CSP_PRFREF', 'CSP_CCAREF', 'CSP_PAFREF', 'CSP_UNIT'],
     'cvs': ['CVS_ID', 'CVS_TYPE', 'CVS_SOURCE', 'CVS_START', 'CVS_INTERVAL', 'CVS_SPID', 'CVS_UNCERTAINTY'],
    'cve': ['CVE_CVSID', 'CVE_PARNAM', 'CVE_INTER', 'CVE_VAL', 'CVE_TOL', 'CVE_CHECK'],
    'cvp': ['CVP_TASK', 'CVP_TYPE', 'CVP_CVSID'],
    'pst': ['PST_NAME', 'PST_DESCR'],
    'psv': ['PSV_NAME', 'PSV_PVSID', 'PSV_DESCR'],
    'cps': ['CPS_NAME', 'CPS_PAR', 'CPS_BIT'],
    'pvs': ['PVS_ID', 'PVS_PSID', 'PVS_PNAME', 'PVS_INTER', 'PVS_VALS', 'PVS_BIT'],
    'psm': ['PSM_NAME', 'PSM_TYPE', 'PSM_PARSET'],
    'cca': ['CCA_NUMBR', 'CCA_DESCR', 'CCA_ENGFMT', 'CCA_RAWFMT', 'CCA_RADIX', 'CCA_UNIT', 'CCA_NCURVE'],
    'ccs': ['CCS_NUMBR', 'CCS_XVALS', 'CCS_YVALS'],
    'paf': ['PAF_NUMBR', 'PAF_DESCR', 'PAF_RAWFMT', 'PAF_NALIAS'],
    'pas': ['PAS_NUMBR', 'PAS_ALTXT', 'PAS_ALVAL'],
    'prf': ['PRF_NUMBR', 'PRF_DESCR', 'PRF_INTER', 'PRF_DSPFMT', 'PRF_RADIX', 'PRF_NRANGE', 'PRF_UNIT'],
    'prv': ['PRV_NUMBR', 'PRV_MINVAL', 'PRV_MAXVAL']
}


# Global variables to track the selected item
selected_cell_value = None
current_tab_index = 0
current_row_index = None

# Function to log messages in the log window
def log_message(message):
    log_textbox.insert(tk.END, message + '\n')
    log_textbox.see(tk.END)  # Scroll to the end of the log

# Function to handle double-click and highlight the selected cell
def on_double_click(event):
    global selected_cell_value
    tree = event.widget
    region = tree.identify("region", event.x, event.y)
    
    if region == "cell":
        row_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)
        
        # Get the row's values and the column index
        row_values = tree.item(row_id, "values")
        col_idx = int(column_id.replace('#', '')) - 1
        
        # Highlight the selected cell (set focus visually)
        tree.selection_set(row_id)
        tree.focus(row_id)
        tree.see(row_id)
        
        # Get the value of the selected cell
        selected_cell_value = row_values[col_idx]
        log_message(f"Selected cell value: {selected_cell_value}")

# Function to handle copying the selected cell value
def copy_to_clipboard(event):
    if selected_cell_value:
        root.clipboard_clear()
        root.clipboard_append(selected_cell_value)
        log_message(f"Copied to clipboard: {selected_cell_value}")
    else:
        log_message("No cell selected to copy.")

# Function to search through tabs and highlight the search keyword
def search_keyword():
    global current_tab_index, current_row_index
    
    keyword = search_entry.get().strip()
    if not keyword:
        log_message("Please enter a search keyword.")
        return

    case_sensitive = case_sensitive_var.get()  # Get the state of case-sensitive checkbox
    
    # Get the number of tabs
    num_tabs = len(notebook.tabs())
    if num_tabs == 0:
        log_message("No tabs to search.")
        return

    # Start searching from the current tab and row
    for tab_offset in range(num_tabs):
        tab_index = (current_tab_index + tab_offset) % num_tabs
        notebook.select(tab_index)

        # Retrieve the frame and the Treeview inside it
        frame = notebook.nametowidget(notebook.tabs()[tab_index])
        tree = frame.winfo_children()[0]  # Assuming Treeview is the first child of the frame
        row_ids = tree.get_children()

        # Determine the starting row for the current tab
        start_row = 0 if tab_index != current_tab_index or current_row_index is None else current_row_index + 1

        # Search through rows in the current tab
        for row_index in range(start_row, len(row_ids)):
            row_values = tree.item(row_ids[row_index], 'values')
            
            # Apply case sensitivity based on checkbox
            if case_sensitive:
                if any(keyword in str(value) for value in row_values):
                    tree.selection_set(row_ids[row_index])  # Select the row
                    tree.focus(row_ids[row_index])  # Focus on the row
                    tree.see(row_ids[row_index])  # Scroll to the row
                    log_message(f"Keyword '{keyword}' found in tab '{notebook.tab(tab_index, 'text')}'.")
                    
                    # Update search state for the next search
                    current_tab_index = tab_index
                    current_row_index = row_index
                    return
            else:
                # Case-insensitive comparison
                if any(keyword.lower() in str(value).lower() for value in row_values):
                    tree.selection_set(row_ids[row_index])  # Select the row
                    tree.focus(row_ids[row_index])  # Focus on the row
                    tree.see(row_ids[row_index])  # Scroll to the row
                    log_message(f"Keyword '{keyword}' found in tab '{notebook.tab(tab_index, 'text')}'.")
                    
                    # Update search state for the next search
                    current_tab_index = tab_index
                    current_row_index = row_index
                    return

        # If no match is found, reset the row index for the next tab
        current_row_index = None

    log_message(f"Keyword '{keyword}' not found.")

# Function to open and display all .dat files from a selected folder
def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Get all .dat files in the folder
        dat_files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

        # Clear existing tabs
        for tab in notebook.tabs():
            notebook.forget(tab)

        # Create a new tab for each .dat file
        for dat_file in dat_files:
            file_path = os.path.join(folder_path, dat_file)
            file_key = os.path.splitext(dat_file)[0]  # Get file name without extension

            try:
                # Open and read the file manually
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                # Split lines into fields and determine the maximum number of columns
                rows = [line.strip().split('\t') for line in lines]
                max_columns = max(len(row) for row in rows)

                # Get the corresponding headers or create generic headers
                if file_key in file_headers:
                    headers = file_headers[file_key]
                else:
                    headers = [f"Column_{i+1}" for i in range(max_columns)]

                # If there are more columns than headers, add extra headers
                if max_columns > len(headers):
                    extra_headers = [f"Extra_{i+1}" for i in range(max_columns - len(headers))]
                    headers.extend(extra_headers)

            except Exception as e:
                log_message(f"Could not process file {dat_file}: {e}")
                continue  # Skip to the next file

            # Create a new frame for each .dat file
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=dat_file)

            # Create a Treeview widget to display the .dat content
            tree = ttk.Treeview(frame, show="headings")

            # Create horizontal and vertical scrollbars for the Treeview
            h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

            # Pack scrollbars and treeview into the frame
            h_scroll.pack(side="bottom", fill="x")
            v_scroll.pack(side="right", fill="y")
            tree.pack(expand=True, fill="both")

            # Set columns in the Treeview with the correct headers
            tree["column"] = headers
            tree["show"] = "headings"

            for col in headers:
                tree.heading(col, text=col)  # Set column headers
                tree.column(col, width=100, minwidth=100, stretch=False)

            # Insert rows into the Treeview
            for row in rows:
                # If a row has fewer values than headers, pad it with empty strings
                if len(row) < len(headers):
                    row += [''] * (len(headers) - len(row))
                tree.insert("", "end", values=row)

            # Bind double-click event to highlight and copy cell content to clipboard
            tree.bind("<Double-1>", on_double_click)

# Create tkinter window
root = tk.Tk()
root.title("MIB Viewer")  # Changed the title to "MIB Viewer"

# Set window size to 800x600
root.geometry("800x600")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create a frame for search functionality
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

# Case-sensitive checkbox
case_sensitive_var = tk.IntVar(value=0)  # Default to case-insensitive (0)
case_sensitive_check = tk.Checkbutton(search_frame, text="Case Sensitive", variable=case_sensitive_var)
case_sensitive_check.pack(side='left', padx=5)

# Search entry box
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side='left', padx=10)

# Search button
search_button = tk.Button(search_frame, text="Search", command=search_keyword)
search_button.pack(side='left')

# Create a button to load the folder containing .dat files
button = tk.Button(root, text="Open Folder", command=open_folder)
button.pack()

# Create a log text box at the bottom
log_textbox = tk.Text(root, height=8, wrap='word', state='normal')
log_textbox.pack(fill='both', padx=10, pady=5)

# Bind Ctrl+C to copy the selected cell value
root.bind('<Control-c>', copy_to_clipboard)

root.mainloop()
