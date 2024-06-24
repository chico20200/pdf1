from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def restructure_pages(pdf_data):
    pdf_reader = PdfReader(BytesIO(pdf_data))
    page_groups = split_pages_groups(pdf_reader.pages)
    merge_pdf = []

    for group in page_groups:
        rearrange_group = rearrange_pages(group)
        for page in rearrange_group:
            merge_pdf.append(page)

    print("Reestructurado exitoso")
    return merge_pdf

def split_pages_groups(pages):
    num_pages = len(pages)
    page_groups = []

    for i in range(0, num_pages, 16):
        actual_group = []
        for j in range(16):
            if i + j < num_pages:
                actual_group.append(pages[i + j])
        page_groups.append(actual_group)
    return page_groups

def rearrange_pages(page_group):
    rearrange_group = []
    num_pages = len(page_group)
    for i in range(num_pages // 2):
        rearrange_group.append(page_group[num_pages - i - 1])
        rearrange_group.append(page_group[i])
    if num_pages % 2 != 0:
        rearrange_group.append(page_group[num_pages // 2])

    return rearrange_group

def add_custom_page(input_pdf_list, custom_page):
    custom_data = open(custom_page, "rb").read()
    with BytesIO(custom_data) as custom_file:
        custom_pdf = PdfReader(custom_file)
        custom = custom_pdf.pages[0]

        pdf_writer_list = PdfWriter()
        for page in input_pdf_list:
            pdf_writer_list.add_page(page)
            pdf_writer_list.add_page(custom)

    print("Diseño añadido exitosamente")
    return pdf_writer_list

def remove_pages(pdf_data, pages_to_remove):
    pdf_reader = PdfReader(BytesIO(pdf_data))
    output_pdf = PdfWriter()
    
    num_pages = len(pdf_reader.pages)
    pages_to_remove_set = set()
    
    for page in pages_to_remove:
        if isinstance(page, int):
            if 0 <= page < num_pages:
                pages_to_remove_set.add(page)
        elif isinstance(page, tuple) and len(page) == 2:
            start, end = page
            for i in range(start, end + 1):
                if 0 <= i < num_pages:
                    pages_to_remove_set.add(i)
    
    for i in range(num_pages):
        if i not in pages_to_remove_set:
            output_pdf.add_page(pdf_reader.pages[i])
    
    output_bytes = BytesIO()
    output_pdf.write(output_bytes)
    print("Páginas removidas exitosamente")
    return output_bytes.getvalue()

def parse_pages_to_remove(pages_str):
    pages = []
    ranges = pages_str.split(',')
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            pages.append((start - 1, end - 1))  # convert to zero-based index
        else:
            pages.append(int(r) - 1)  # convert to zero-based index
    return pages

def main():
    input_pdf = "Edda_Menor.pdf"
    custom_page_input = "customPageMitologica.pdf"
    output_pdf = "Eda_Menor_Para_Notas.pdf"
    
    pages_str = input("Ingresa las páginas o rangos de páginas a eliminar (por ejemplo, '1, 3-5, 10-12'): ")
    pages_to_remove = parse_pages_to_remove(pages_str)

    with open(input_pdf, "rb") as file:
        file_data = file.read()
        
        file_data = remove_pages(file_data, pages_to_remove)
        restructured_pdf = restructure_pages(file_data)
        pdf_for_notes = add_custom_page(restructured_pdf, custom_page_input)

        with open(output_pdf, "wb") as output_file:
            pdf_for_notes.write(output_file)

    print("Se logró crear el archivo")

if __name__ == "__main__":
    main()
