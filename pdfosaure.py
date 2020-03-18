# Pdfosaure - Hungry dino tooling up pdfs
# Copyright (C) 2020 Yoann Pietri

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Pdfosaure.

To see examples and extended documentation, please visit https://github.com/nanoy42/pdfosaure

Usage:
  pdfosaure.py infos <filename>
  pdfosaure.py encrypt <filename> [<output>]
  pdfosaure.py decrypt <filename> [<output>]
  pdfosaure.py rotate <filename> <angle> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
  pdfosaure.py scale <filename> <factor> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
  pdfosaure.py compress <filename> [<output>] [--stats]
  pdfosaure.py deletepages <filename> <pages> [<output>]
  pdfosaure.py merge <filenames> <filenames>... [--output_filename=<output>]
  pdfosaure.py explode <filename> [--output=<output_scheme>]
  pdfosaure.py split <filename> <pages> [--output=<output_scheme>]
  pdfosaure.py pdftojpeg <filename> [<pages>] [--output=<output_scheme>]
  pdfosaure.py jpegtopdf <filenames>... [--output_filename=<output>]
  pdfosaure.py (-h | --help)
  pdfosaure.py --version

Options:
  <filename>                  Refers to the filename of the input pdf file
  <output>                    Refers to the filename of the output pdf file. By default, the script overwrites the input pdf.
  <angle>                     Rotation angle. Should be a multiple of 90. The rotation is clockwise.
  --include=<pages_in>        List of pages on which the effect should apply. The pages should be seperated by commas (,) without spaces. Cannot be use with --exclude.
  --exclude=<pages_out>       List of pages on which the effect should not apply. The pages should be seperated by commas (,) without spaces. Cannot be use with --include.
  --stats                     Print before and after sizes when compressing.
  <pages>                     List of pages on which the effect should apply. The pages should be separated by commas (,) without spaces.
  <filenames>                 Refers to one or more input filename (when merging pdfs of jpegs by instance).
  --output_filename=<output>  Refers to the filename of the output pdf file. By default, the script overwrites the input pdf.
  --output=<output_scheme>    When multiple files are generated, the names of output files look like {output_scheme}-{number}.{extension}
  -h --help                   Show this screen.
  --version                   Show version.

"""
import getpass
import os

import img2pdf
from docopt import docopt
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter


def get_infos(filename):
    pdf = PdfFileReader(open(filename, "rb"))
    infos = pdf.getDocumentInfo()
    msg = """
    Author : {}
    Creation date : {}
    Creator: {}
    Keywords: {}
    Modification date : {}
    Producer : {}
    Subject : {}
    Title : {}
    Number of pages : {}
    Encrypted : {}
    """.format(
        infos["/Author"],
        infos["/CreationDate"],
        infos["/Creator"],
        infos["/Keywords"],
        infos["/ModDate"],
        infos["/Producer"],
        infos["/Subject"],
        infos["/Title"],
        pdf.getNumPages(),
        pdf.isEncrypted,
    )
    return msg


def write(output, filename, output_filename):
    """Write output pdf to output_filename

    A trick is needed if the output_filename is the same as the original filename
    
    Args:
        output (PdfFileWriter): PdfFileWriter to write
        filename (string): Original filename
        output_filename (string): filename of the output file
    """
    if output_filename == filename:
        output.write(open("temp.pdf", "wb"))
        os.rename("temp.pdf", filename)
    else:
        output.write(open(output_filename, "wb"))


def encrypt(filename, password, output_filename):
    """Encrypt a pdf file
    
    Args:
        filename (string): filename of the input pdf file
        password (string): password for encryption
        output_filename (string): filename of the output pdf file
    """
    pdf = PdfFileReader(open(filename, "rb"))
    if pdf.isEncrypted:
        print("PDF is already encrypted")
        exit()
    else:
        output = PdfFileWriter()
        output.appendPagesFromReader(pdf)
        output.encrypt(password)
        write(output, filename, output_filename)


def decrypt(filename, password, output_filename):
    """Decrupt a pdf file
    
    Args:
        filename (string): filename of the input pdf file
        password (string): password for encryption
        output_filename (string): filename of the output pdf file
    """
    pdf = PdfFileReader(open(filename, "rb"))
    if not pdf.isEncrypted:
        print("PDF is not encrypted")
        exit()
    else:
        output = PdfFileWriter()
        pdf.decrypt(password)
        output.appendPagesFromReader(pdf)
        write(output, filename, output_filename)


def rotate_pages(filename, angle, include, exclude, output_filename):
    """Rotate pages of a given angle.

    Pages are specified either by include parameter (which pages should be rotated)
    or by exclude paramater (which pages sould not be rotated). Angle should be 
    a multiple of 90.
    
    Args:
        filename (string): filename of the input pdf file
        angle (int): rotation angle. Should be a multiple of 90.
        include (list of int): list of pages to rotate
        exclude (list of int): list of pages to not rotate
        output_filename (string): filename of the output pdf file
    """
    pdf = PdfFileReader(open(filename, "rb"))
    if angle % 90 != 0:
        print("Rotation angle muste be a multiple of 90")
        exit()
    else:
        output = PdfFileWriter()
        if include and not exclude:
            for i in range(pdf.getNumPages()):
                page = pdf.getPage(i)
                if i + 1 in include:
                    page.rotateClockwise(angle)
                output.addPage(page)
        elif exclude and not include:
            for i in range(pdf.getNumPages()):
                page = pdf.getPage(i)
                if i + 1 not in exclude:
                    page.rotateClockwise(angle)
                output.addPage(page)
    write(output, filename, output_filename)


def rotate_all_pages(filename, angle, output_filename):
    """Rotate all pages of a given angle.

    The angle should be a multiple of 90.
    
    Args:
        filename (string): filename of the input pdf file.
        angle (int): rotation angle. Should be a multiple of 90.
        output_filename (string): filename of the output pdf file.
    """
    if angle % 90 != 0:
        print("Rotation angle muste be a multiple of 90")
        exit()
    output = PdfFileWriter()
    pdf = PdfFileReader(open(filename, "rb"))
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        page.rotateClockwise(angle)
        output.addPage(page)
    write(output, filename, output_filename)


def scale_pages(filename, include, exclude, scale_x, scale_y, output_filename):
    """Scale given pages by x and y factors

    Pages are specified either by include parameter (which pages should be scaled)
    or by exclude paramater (which pages sould not be scaled).    
    
    Args:
        filename (string): filename of the input pdf file
        include (list of int): list of pages to scale.
        exclude (list of int): list of pages to not scale.
        scale_x (float): scale factor in x direction.
        scale_y (float): scale factor in y direction.
        output_filename (srting): filename of the output pdf file.
    """
    pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    if include and not exclude:
        for i in range(pdf.getNumPages()):
            page = pdf.getPage(i)
            if i + 1 in include:
                page.scale(scale_x, scale_y)
            output.addPage(page)
    elif exclude and not include:
        for i in range(pdf.getNumPages()):
            page = pdf.getPage(i)
            if i + 1 not in exclude:
                page.scale(scale_x, scale_y)
            output.addPage(page)
    write(output, filename, output_filename)


def scale_all_pages(filename, scale_x, scale_y, output_filename):
    """Scale all pages by x and y factors.
    
    Args:
        filename (string): filename of the input pdf file.
        scale_x (int): scale factor in x direction.
        scale_y (int): scale factor in y direction.
        output_filename (string): filename of the output pdf file.
    """
    pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        page.scale(scale_x, scale_y)
        output.addPage(page)
    write(output, filename, output_filename)


def compress(filename, output_filename):
    """Compress pdf file.
    
    Args:
        filename (string): filename of the input pdf file.
        output_filename (string): filename of the output pdf file.
    """
    pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        page.compressContentStreams()
        output.addPage(page)
    write(output, filename, output_filename)


def merge(output_filename, *args):
    """Merge pdf files.
    
    Args:
        output_filename (string): filename of the output pdf file.
        *args (strings): filenames of input pdf files.
    """
    output = PdfFileWriter()
    for arg in args:
        pdf = PdfFileReader(open(arg, "rb"))
        output.appendPagesFromReader(pdf)
    with open(output_filename, "wb") as f:
        output.write(f)


def explode(filename, output_scheme):
    """Create 1 pdf file for page in input pdf.
    
    Args:
        filename (string): filename of the input pdf file.
        output_scheme (string): pdf files will have the following name: {output_scheme}-{number}.pdf
    """
    pdf = PdfFileReader(open(filename, "rb"))
    for i in range(pdf.getNumPages()):
        output = PdfFileWriter()
        page = pdf.getPage(i)
        output.addPage(page)
        output.write(open("{}-{}.pdf".format(output_scheme, i + 1), "wb"))


def split(filename, pages, output_scheme):
    """Create 1 pdf file for each range of page specified by pages.
    
    Args:
        filename (string): filename of the input pdf file.
        pages (list of ints): delimiters of ranges.
        output_scheme (string): pdf files will have the following name: {output_scheme}-{number}.pdf
    """
    pdf = PdfFileReader(open(filename, "rb"))
    pages.insert(0, 0)
    pages.append(pdf.getNumPages())
    for i in range(len(pages) - 1):
        output = PdfFileWriter()
        for j in range(pages[i], pages[i + 1] - 1):
            page = pdf.getPage(j)
            output.addPage(page)
        output.write(open("{}-{}.pdf".format(output_scheme, i + 1), "wb"))


def pdf_to_jpeg_pages(filename, pages, output_scheme):
    """Export given pages to jpeg files.
    
    Args:
        filename (string): filename of the input pdf file.
        pages (list of ints): pages to export.
        output_scheme (string): jpeg files will have the following name: {output_scheme}-{number}.jpg
    """
    images = convert_from_path(filename, 500)
    for i, image in enumerate(images):
        if i + 1 in pages:
            image.save("{}-{}.jpg".format(output_scheme, i + 1), "JPEG")


def pdf_to_jpeg_all_pages(filename, output_scheme):
    """Export all pages of a pdf file to jpeg images.
    
    Args:
        filename (string): filename of the input pdf file.
        output_scheme (string): images will have the following name: {output_scheme}-{number}.jpg
    """
    images = convert_from_path(filename, 500)
    for i, image in enumerate(images):
        image.save("{}-{}.jpg".format(output_scheme, i + 1), "JPEG")


def jpegs_to_pdf(output_filename, *args):
    """Merge jpeg images in one pdf file.
    
    Args:
        output_filename (string): filename of the ouput pdf file
        *args (strings): filename of jpeg files.
    """
    with open(output_filename, "wb") as f:
        f.write(img2pdf.convert([arg for arg in args]))


def delete_pages(filename, pages, output_filename):
    """Delete given pages
    
    Args:
        filename (string): filename of the the input pdf file.
        pages (list of ints): pages to delete.
        output_filename (string): filename of the output pdf file. 
    """
    pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        if i + 1 not in pages:
            output.addPage(page)
    write(output, filename, output_filename)


def get_size(filename):
    """Get size of a file
    
    Args:
        filename (string): filename of file to get size.
    
    Returns:
        int: size of the file.
    """
    input_stream = open(filename, "rb")
    input_stream.seek(0, 2)
    size = input_stream.tell()
    input_stream.close()
    return size


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Pdfosaure 0.1")
    if arguments["infos"]:
        print(get_infos(arguments["<filename>"]))
    elif arguments["encrypt"]:
        password = getpass.getpass()
        encrypt(
            arguments["<filename>"],
            password,
            arguments["<output>"] or arguments["<filename>"],
        )
    elif arguments["decrypt"]:
        password = getpass.getpass()
        decrypt(
            arguments["<filename>"],
            password,
            arguments["<output>"] or arguments["<filename>"],
        )
    elif arguments["rotate"]:
        if not arguments["--include"] and not arguments["--exclude"]:
            rotate_all_pages(
                arguments["<filename>"],
                int(arguments["<angle>"]),
                arguments["<output>"] or arguments["<filename>"],
            )
        elif arguments["--include"] and arguments["--exclude"]:
            print("You cannot use inlcude and exclude")
        else:
            rotate_pages(
                arguments["<filename>"],
                int(arguments["<angle>"]),
                [int(p) for p in arguments["--include"].split(",")],
                [int(p) for p in arguments["--exclude"].split(",")],
                arguments["<output>"] or arguments["<filename>"],
            )
    elif arguments["scale"]:
        if not arguments["--include"] and not arguments["--exclude"]:
            scale_all_pages(
                arguments["<filename>"],
                float(arguments["<factor>"]),
                float(arguments["<factor>"]),
                arguments["<output>"] or arguments["<filename>"],
            )
        elif arguments["--include"] and arguments["--exclude"]:
            print("You cannot use inlcude and exclude")
        else:
            scale_pages(
                arguments["<filename>"],
                float(arguments["<factor>"]),
                float(arguments["<factor>"]),
                [int(p) for p in arguments["--include"].split(",")],
                [int(p) for p in arguments["--exclude"].split(",")],
                arguments["<output>"] or arguments["<filename>"],
            )
    elif arguments["compress"]:
        if arguments["--stats"]:
            size1 = get_size(arguments["<filename>"])
        compress(
            arguments["<filename>"], arguments["<output>"] or arguments["<filename>"]
        )
        if arguments["--stats"]:
            size2 = get_size(arguments["<output>"] or arguments["<filename>"])
            print("Before compression : {}".format(size1))
            print("After compression : {}".format(size2))
            print("Difference : {}".format(size2 - size1))
    elif arguments["deletepages"]:
        delete_pages(
            arguments["<filename>"],
            [int(p) for p in arguments["<pages>"].split(",")],
            arguments["<output>"] or arguments["<filename>"],
        )
    elif arguments["merge"]:
        merge(arguments["--output_filename"] or "output.pdf", *arguments["<filenames>"])
    elif arguments["explode"]:
        explode(arguments["<filename>"], arguments["--output"] or "output")
    elif arguments["split"]:
        split(
            arguments["<filename>"],
            [int(p) for p in arguments["<pages>"].split(",")],
            arguments["--output"] or "output",
        )
    elif arguments["pdftojpeg"]:
        if arguments["<pages>"]:
            pdf_to_jpeg_pages(
                arguments["<filename>"],
                [int(p) for p in arguments["<pages>"].split(",")],
                arguments["--output"] or "output",
            )
        else:
            pdf_to_jpeg_all_pages(
                arguments["<filename>"], arguments["--output"] or "output"
            )
    elif arguments["jpegtopdf"]:
        jpegs_to_pdf(
            arguments["--output_filename"] or "output.pdf", *arguments["<filenames>"]
        )
