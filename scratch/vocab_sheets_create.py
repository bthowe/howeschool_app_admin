import os
from PIL import Image as PilImage

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Image


def png_crop(filename_old, filename_new):
    im = PilImage.open(filename_old)
    w, h = im.size
    im = im.crop((0, 0, w, 375))
    im.save(filename_new)

def number_of_images(directory_name):
    num_o_files = 0
    for file in os.listdir(directory_name):
        if file.endswith(".png"):
            num_o_files += 1
    return num_o_files

def vocab_set_table_create(set_num):
    width = 850 * .15  # 850 total pixels
    height = 375 * .15  # 475

    elements_lst = []
    for i in range(0, number_of_images(f'/Users/travis/Projects/howeschool_app/static/{set_num}/'), 2):
        png_crop(f'/Users/travis/Projects/howeschool_app/static/{set_num}/rc_vocab_{set_num}_{i}.png', f'/Users/travis/Downloads/rc_vocab_{set_num}_{i}.png')
        png_crop(f'/Users/travis/Projects/howeschool_app/static/{set_num}/rc_vocab_{set_num}_{i + 1}.png', f'/Users/travis/Downloads/rc_vocab_{set_num}_{i + 1}.png')
        im1 = Image(f'/Users/travis/Downloads/rc_vocab_{set_num}_{i}.png', width=width, height=height)
        im2 = Image(f'/Users/travis/Downloads/rc_vocab_{set_num}_{i + 1}.png', width=width, height=height)
        elements_lst += [im1, im2]

    table_body = [[f'Vocabulary Set #{set_num}', '', '', '']]
    for i in range(0, len(elements_lst), 4):
        table_body += [elements_lst[i: i + 4]]

    table = Table(table_body)
    style = TableStyle(
        [
            ('SPAN', (0, 0), (3, 0)),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('LINEAFTER', (1, 0), (1, -1), 1, colors.black, None, None, None, 2, 1),
            ('GRID', (0, 1), (-1, -1), 0.25, colors.lightgrey),
        ]
    )
    table.setStyle(style)
    return table

def main():
    pdf = SimpleDocTemplate('/Users/travis/Downloads/rc_vocabulary.pdf', pagesize=letter, leftMargin=35, rightMargin=35, topMargin=15, bottomMargin=25)

    elems = []
    set_lst = list(range(4, 13)) + list(range(14, 150))
    for vocab_set in set_lst:
        elems += [vocab_set_table_create(vocab_set), PageBreak()]
    elems.pop()
    pdf.build(elems)

if __name__ == '__main__':
    main()
