from nicegui import ui, run, app
import os
import glob
from contract_to_txt import convert_to_txt
from flag_FAR_clauses import annotate_contract
from contract_to_txt import convert_to_txt, txt_to_docx
from flag_problem_language import _flag_problem_language
from nltk import data as nltk
import pdf_to_txt

# Append the custom path to the NLTK data path
nltk.path.append("supplementary_files\\nltk_data")

FAR_CLAUSE_MATRIX_PATH = "supplementary_files\\2023-03-20_FAR Matrix.xls"
TNC_MATRIX_PATH = "supplementary_files\\Contract Ts&Cs Matrix.xlsm"

##############################################################################################################################

@ui.page("/subscanner")
def subcontract_scanner():
    ui.add_head_html("<link rel='stylesheet' href='/static/style.css'/>")
    ui.html('<title>AI Contract Review</title>')
    ui.colors(primary='#E87722', secondary='#e86100')
    with ui.header(elevated=True).style('width: 100%; display: flex; justify-content: center;'):
        with ui.element():
            ui.label('Subcontractor Agreement Scanner').style('font-size: 22px; text-align: center')
            with ui.element().style('width: 100%; display: flex; justify-content: center;'):
                ui.label('Office of Sponsored Programs').style('font-size: 18px;')
    ui.upload(multiple=True, label="Upload Subcontractor Agreements", auto_upload=True, on_upload=handle_sub_upload).props(add="accept='.pdf'")

def handle_sub_upload(e):
    name = e.name
    binary = e.content.read()
    upload_filepath = write_binary_to_temp_file(name, binary)
    text_file_name = pdf_to_txt.pdf_to_txt(upload_filepath)
    found = pdf_to_txt.flag_findings(text_file_name)
    if found:
        ui.notify(name + " was flagged", type='negative')
    else:
        ui.notify(name + " was not flagged", type='positive')




##############################################################################################################################

@ui.page("/contractscanner")
def contract_scanner():
    ui.add_head_html("<link rel='stylesheet' href='/static/style.css'/>")
    ui.html('<title>AI Contract Review</title>')
    ui.colors(primary='#0b2341', secondary='#e86100')
    with ui.header(elevated=True).style('width: 100%; display: flex; justify-content: center;'):
        with ui.element():
            ui.label('AI Contract Scanner').style('font-size: 22px; text-align: center')
            with ui.element().style('width: 100%; display: flex; justify-content: center;'):
                ui.label('Office of Sponsored Programs').style('font-size: 18px;')
    ui.upload(multiple=True, label="Upload Contracts", auto_upload=True, on_upload=handle_contract_upload).props(add="accept='.docx,.pdf'")


async def handle_contract_upload(e):
    name = e.name
    binary = e.content.read()
    upload_filepath = write_binary_to_temp_file(name, binary)
    downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    output_filepath = os.path.join(downloads_path, f"{getFilenameStringNoExtension(name)}_scanned.docx")
    ui.notify("Scanning file...")
    await run.cpu_bound(scan_file, upload_filepath, output_filepath)
    os.remove(upload_filepath)
    ui.notify("Downloading scan")
    ui.download(output_filepath)

def scan_file(filepath, output_filepath):
    # clean docx and annotate it
    convert_to_txt(filepath)
    _flag_problem_language(TNC_MATRIX_PATH)
    back_to_docx = 'flagged_contract_to_txt.txt'
    file_to_highlight = 'flagged_contract_to_docx.docx'
    txt_to_docx(back_to_docx, file_to_highlight)

    annotate_contract(FAR_CLAUSE_MATRIX_PATH, file_to_highlight, output_filepath)

def getFilenameStringNoExtension(filename):
    temp_list = filename.split(".")
    if (len(temp_list) == 1):
        return temp_list[0]
    else:
        temp_list.pop()
        return '.'.join(temp_list)

def write_binary_to_temp_file(name, binary):
    filepath = f"temp/{name}"
    with open(file=filepath, mode="wb") as file:
        file.write(binary)
    return filepath

##########################################################################################

@ui.page("/")
def index():
    ui.add_head_html("<link rel='stylesheet' href='/static/style.css'/>")
    ui.label("Choose the feature you would like to access:").style("font-size: 30px;")
    with ui.element().style("""
                            display: flex;
                            width: 100vw;
                            justify-content: center;
                            height: calc(100vh - 50px);
                            align-items: center;
                            position: absolute;
                            top: 50px;
                            left: 0;"""):
        ui.link("AI Contract Scanner", contract_scanner).classes("page-button").style("background: #0b2341; margin-right: 50px;")
        ui.link("Subcontractor Agreement Scanner", subcontract_scanner).classes("page-button").style("background: #E87722;")

if __name__ in {"__main__", "__mp_main__"}:
    app.add_static_files("/static", "static")
    app.add_static_files("/temp", "temp")
    ui.run(reload=False, host="0.0.0.0")