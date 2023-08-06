"""
Converter module for dost. This module contains functions to convert between different data types.

Examples:
    >>> from dost import converter
    >>> converter.convert_csv_to_excel('tests\\demo.csv', 'tests\\demo.xlsx')
    >>> converter.get_image_from_base64('tests\\demo.txt')
    >>> converter.get_base64_from_image('tests\\demo.png')
    >>> converter.excel_change_corrupt_xls_to_xlsx('tests\\demo.xls', 'tests\\demo.xlsx')
    >>> converter.excel_convert_xls_to_xlsx('tests\\demo.xls', 'tests\\demo.xlsx')
    >>> converter.convert_image_jpg_to_png('tests\\demo.jpg', 'tests\\demo.png')
    >>> converter.convert__image_png_to_jpg('tests\\demo.png', 'tests\\demo.jpg')
    >>> converter.excel_to_colored_html('tests\\demo.xlsx', 'tests\\demo.html')


The module contains the following functions:

- `convert_csv_to_excel(csv_path, excel_path)`: Convert a CSV file to an Excel file.
- `get_image_from_base64(path)`: Get an image from a base64 encoded string.
- `get_base64_from_image(path)`: Get a base64 encoded string from an image.
- `excel_change_corrupt_xls_to_xlsx(xls_path, xlsx_path)`: Change a corrupt XLS file to an XLSX file.
- `excel_convert_xls_to_xlsx(xls_path, xlsx_path)`: Convert an XLS file to an XLSX file.
- `convert_image_jpg_to_png(jpg_path, png_path)`: Convert a JPG image to a PNG image.
- `convert__image_png_to_jpg(png_path, jpg_path)`: Convert a PNG image to a JPG image.
- `excel_to_colored_html(excel_path, html_path)`: Convert an Excel file to a colored HTML file.

"""


import os
from pathlib import WindowsPath
from dost.helpers import dostify
from typing import Union, List

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-DOST', 'Converters Folder')

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


@dostify(errors=[(FileNotFoundError, '')])
def convert_csv_to_excel(input_filepath: Union[str, WindowsPath], output_folder: Union[str, WindowsPath] = "", output_filename: str = "", contains_headers: bool = True, sep: str = ","):
    """Convert a CSV file to an Excel file.

    Args:
        input_filepath (str,WindowsPath): The path to the CSV file.
        output_folder (str,WindowsPath): The path to the output folder.
        output_filename (str): The name of the output file.
        contains_headers (bool): Whether the CSV file contains headers.
        sep (str): The separator used in the CSV file.

    Examples:
        >>> convert_csv_to_excel('tests\\demo.csv')


    """
    # Import Section
    import os
    from pathlib import Path
    import pandas as pd
    import datetime

    # Code Section
    if not input_filepath:
        raise Exception("CSV File name cannot be empty")

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = "excel_" + \
            str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx"
    else:
        if (output_filename.endswith(".xlsx")):
            output_filename = output_filename
        else:
            output_filename = output_filename+".xlsx"
    if not sep:
        raise Exception("Separator cannot be empty")

    excel_file_path = os.path.join(
        output_folder, output_filename)
    excel_file_path = Path(excel_file_path)
    writer = pd.ExcelWriter(excel_file_path)
    headers = 'infer'
    if contains_headers == False:
        headers = None
    df = pd.read_csv(input_filepath, sep=sep, header=headers)
    df.to_excel(writer, sheet_name='Sheet1',
                index=False, header=contains_headers)
    writer.save()
    writer.close()


@dostify(errors=[])
def get_image_from_base64(input_text: str, output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Get an image from a base64 encoded string.

    Args:
        input_text (str): The base64 encoded string.
        output_folder (str,WindowsPath): The path to the output folder.
        output_filename (str default ending with .png): The name of the output file.

    Examples:
        >>> get_image_from_base64('"base_64_string')

    """
    # Import Section
    import base64
    import os
    import datetime

    # Code Section
    if not input_text:
        raise Exception("Image base64 string cannot be empty")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = "image_" + \
            str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png"
    else:
        if not (str(output_filename).endswith(".png") or str(output_filename).endswith(".jpg")):
            output_filename = output_filename + ".png"
        else:
            output_filename = output_filename

    input_text = bytes(input_text, 'utf-8')
    if os.path.exists(output_folder):
        img_binary = base64.decodebytes(input_text)
        with open(os.path.join(output_folder, output_filename), "wb") as f:
            f.write(img_binary)
    else:
        raise Exception("Image folder path does not exist")


@dostify(errors=[(FileNotFoundError, '')])
def convert_image_to_base64(input_filepath: Union[str, WindowsPath]):
    """Get a base64 encoded string from an image.

    Args:
        input_filepath (str,WindowsPath): The path to the image file.

    Examples:
        >>> convert_image_to_base64('tests\\demo.png')

    """
    # Import section
    import base64
    import os

    # Code section
    if not input_filepath:
        raise Exception("Image file name cannot be empty")

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if os.path.exists(input_filepath):
        with open(input_filepath, "rb") as f:
            data = base64.b64encode(f.read())
    else:
        raise Exception("Image file does not exist")
    return data


@dostify(errors=[(FileNotFoundError, '')])
def excel_change_corrupt_xls_to_xlsx(input_filepath: Union[str, WindowsPath], input_sheetname: str, output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Change a corrupt XLS file to an XLSX file.

    Args:
        input_filepath (str,WindowsPath): The path to the corrupt XLS file.
        input_sheetname (str): The name of the sheet in the corrupt XLS file.
        output_folder (str,WindowsPath): The path to the output folder.
        output_filename (str): The name of the output file.

    Examples:
        >>> excel_change_corrupt_xls_to_xlsx('tests\\demo.xls', 'Sheet1')

    """
    # Import section
    import os

    import io
    from xlwt import Workbook
    from xls2xlsx import XLS2XLSX
    import datetime
    from pathlib import Path

    # Code section
    if not input_filepath:
        raise Exception("XLS File name cannot be empty")

    if not os.path.exists(input_filepath) == False:
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not input_sheetname:
        raise Exception("XLS Sheet name cannot be empty")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = os.path.join(output_folder, str(Path(input_filepath).stem) + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx")
    else:
        if (output_filename.endswith(".xlsx")):
            output_filename = os.path.join(output_folder, output_filename)
        else:
            output_filename = os.path.join(
                output_folder, output_filename+".xlsx")

    # Opening the file
    file1 = io.open(input_filepath, "r")
    data = file1.readlines()

    # Creating a workbook object
    xldoc = Workbook()
    # Adding a sheet to the workbook object
    sheet = xldoc.add_sheet(input_sheetname, cell_overwrite_ok=True)
    # Iterating and saving the data to sheet
    for i, row in enumerate(data):
        # Two things are done here
        # Removing the '\n' which comes while reading the file using io.open
        # Getting the values after splitting using '\t'
        for j, val in enumerate(row.replace('\n', '').split('\t')):
            sheet.write(i, j, val)

    # Saving the file as a normal xls excel file
    xldoc.save(input_filepath)

    # checking the downloaded file is present or not
    if os.path.exists(input_filepath):
        # converting xls to xlsx
        x2x = XLS2XLSX(input_filepath)
        x2x.to_xlsx(output_filename)


@dostify(errors=[(FileNotFoundError, '')])
def excel_convert_xls_to_xlsx(input_filepath: Union[str, WindowsPath], output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Convert an XLS file to an XLSX file.

    Args:
        input_filepath (str,WindowsPath): The path to the XLS file.
        output_folder (str,WindowsPath): The path to the output folder.
        output_filename (str): The name of the output file.

    Examples:
        >>> excel_convert_xls_to_xlsx('tests\\demo.xls')

    """
    # Import section
    import os
    from xls2xlsx import XLS2XLSX
    from pathlib import Path
    import datetime

    # Code section
    if not input_filepath:
        raise Exception("XLS File name cannot be empty")
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = os.path.join(output_folder, str(Path(input_filepath).stem), str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx")
    else:
        if (output_filename.endswith("xlsx")):
            output_filename = os.path.join(output_folder, output_filename)
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename)+".xlsx")

    # Checking the path and then converting it to xlsx file
    if os.path.exists(input_filepath):
        # converting xls to xlsx
        x2x = XLS2XLSX(input_filepath)
        x2x.to_xlsx(output_filename)


@dostify(errors=[(FileNotFoundError, '')])
def convert_image_jpg_to_png(input_filepath: Union[str, WindowsPath], output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Convert a JPG image to a PNG image.

    Args:
        input_filepath (str,WindowsPath): The path to the JPG image.
        output_folder (str,WindowsPath): The path to the output folder.
        output_filename (str): The name of the output file.

    Examples:
        >>> convert_image_jpg_to_png('tests\\demo.jpg')

    """
    # import section
    from pathlib import Path
    import os
    from PIL import Image
    import datetime

    # Code section
    if not input_filepath:
        raise Exception("Enter the valid input image path")

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = os.path.join(output_folder, str(Path(input_filepath).stem) + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png")
    else:
        if output_filename.endswith(".png"):
            output_filename = os.path.join(output_folder, str(output_filename))
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename)+".png")
    im = Image.open(input_filepath)
    rgb_im = im.convert('RGB')
    rgb_im.save(output_filename)


@dostify(errors=[(FileNotFoundError, '')])
def convert__image_png_to_jpg(input_filepath: Union[str, WindowsPath], output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Converts the image from png to jpg format

    Args:
        input_filepath (str,WindowsPath): Input image file path
        output_folder (str,WindowsPath): Output folder path
        output_filename (str): Output file name

    Examples:
        >>> convert__image_png_to_jpg('tests\\demo.png')

    """
    # Import Section
    from pathlib import Path
    import os
    from PIL import Image
    import datetime

    # Code Section
    if not input_filepath:
        raise Exception("Enter the valid input image path")

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = os.path.join(output_folder, str(Path(input_filepath).stem) + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".jpg")
    else:
        if output_filename.endswith(".jpg"):
            output_filename = os.path.join(output_folder, str(output_filename))
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename)+".jpg")

    im = Image.open(input_filepath)
    rgb_im = im.convert('RGB')
    rgb_im.save(output_filename)


@dostify(errors=[(FileNotFoundError, '')])
def excel_to_colored_html(input_filepath: Union[str, WindowsPath], output_folder: Union[str, WindowsPath] = "", output_filename: str = ""):
    """Converts the excel file to colored html file

    Args:
        input_filepath (str,WindowsPath): Input excel file path
        output_folder (str,WindowsPath): Output folder path
        output_filename (str): Output file name

    Examples:
        >>> excel_to_colored_html('tests\\demo.xlsx')
    """
    # Import Section
    from pathlib import Path
    from xlsx2html import xlsx2html
    import datetime

    # Code Section
    if not input_filepath:
        raise Exception("Please provide the excel path")

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"File not found at path {input_filepath}")

    if not output_folder:
        output_folder = output_folder_path

    if not os.path.exists(output_folder):
        # os.makedirs(output_folder)
        raise FileNotFoundError(f"Folder not found at path {output_folder}")

    if not output_filename:
        output_filename = os.path.join(output_folder, str(Path(input_filepath).stem)+'_'+str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".html")
    else:
        if (output_filename.endswith(".html")):
            output_filename = os.path.join(output_folder, str(output_filename))
        else:
            output_filename = os.path.join(
                output_folder, output_filename+'.html')

    xlsx2html(input_filepath, output_filename)

    # os.startfile(output_folder)
# convert_image_jpg_to_png(input_filepath='tests\demo2.png',output_folder="testssad",output_filename="demo")
convert_image_jpg_to_png(
    input_filepath='tests\demo2.png', output_folder="testssad")
