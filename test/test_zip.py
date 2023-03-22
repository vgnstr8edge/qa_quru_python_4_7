import os
import csv
import zipfile
from zipfile import ZipFile
from pathlib import Path
import shutil
from openpyxl import load_workbook
from PyPDF2 import PdfReader


current_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.abspath('resources')

pdf_ = os.path.join(current_dir, 'resources/sample.pdf')
xlsx_ = os.path.join(current_dir, 'resources/sample1.xlsx')
csv_ = os.path.join(current_dir, 'resources/username.csv')

list_files = [pdf_, xlsx_, csv_]


def create_zip():
    with zipfile.ZipFile('test.zip', 'w') as zip_:
        for file in list_files:
            zip_.write(file)


def zip_moves():
    for file in Path(current_dir).glob('test.zip'):
        shutil.move(os.path.join(current_dir, file), destination_dir)


def test_check_pdf():
    with ZipFile('resources/test.zip') as zip_:
        zip_.namelist()
        with zip_.open('sample.pdf', 'r'):
            reader = PdfReader('sample.pdf')
            pdf_file = reader.pages[0].extract_text
            assert 'A Simple PDF File' in pdf_file


def test_check_xlsx():
    file_names = []

    with ZipFile('resources/test.zip') as zip_:
        for file in zip_.namelist():
            file_names.append(file)

    for name in file_names:
        if name == 'sample1.xlsx':
            with ZipFile('resources/test.zip') as zip_:
                with zip_.open('sample1.xlsx', 'r'):
                    workbook = load_workbook('sample1.xlsx')
                    sheet = workbook.active
                    row_name = sheet.cell(2, 2).value
                    assert row_name == 'Jane'


def test_check_csv():
    file_names = []

    with ZipFile('resources/test.zip') as zip_:
        for file in zip_.namelist():
            file_names.append(file)

    for name in file_names:
        if name == 'username.csv':
            with ZipFile('resources/test.zip') as zip_:
                with zip_.open('username.csv', 'r') as csv_file:
                    csv_file = csv.reader(csv_file)
                    assert csv_file[0] == ['Username; Identifier;First name;Last name']
