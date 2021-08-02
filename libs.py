import xlsxwriter

FILENAME = 'zlotapolska.xlsx'
COMPLETED_ONES = 'zebrane.txt'
HEADERS = {
    'name': 'Nazwa miejsca',
    'desc': 'Gdzie jest medal',
    'address': 'Adres',
    'distance': 'Dystans',
    'gathered': 'Zebrane',
    'voivodship': 'Województwo',
}

gathered_ones = []


def read_already_gathered_medals():
    """Read already gathered medals information"""
    with open(COMPLETED_ONES, encoding="UTF-8") as file:
        for f in file.readlines():
            gathered_ones.append(f.lower().strip())


def process_row(item, field_id):
    """If distance then save as int otherwise save as string"""
    return int(item.get(field_id, 0)) if field_id == 'distance' else item.get(field_id, '')


def create_xlsx_file(items):
    """Save File to excel"""
    print("Saving File")
    read_already_gathered_medals()
    print(gathered_ones)
    with xlsxwriter.Workbook(FILENAME) as workbook:
        bold = workbook.add_format({'bold': True})
        bgcolor_gathered = workbook.add_format({'bg_color': 'green'})
        worksheet = workbook.add_worksheet()
        worksheet.write_row(row=0, col=0, data=HEADERS.values(), cell_format=bold)
        header_keys = list(HEADERS.keys())
        for index, item in enumerate(items):
            if item.get('name').lower() in gathered_ones:
                item['gathered'] = True
                row = map(lambda field_id: process_row(item, field_id), header_keys)
                worksheet.write_row(row=index + 1, col=0, data=row, cell_format=bgcolor_gathered)
            else:
                item['gathered'] = False
                row = map(lambda field_id: process_row(item, field_id), header_keys)
                worksheet.write_row(row=index + 1, col=0, data=row)
        worksheet.set_column(0, 2, 100)
        worksheet.set_column(3, 4, 10)
        worksheet.set_column(5, 5, 60)
    print("File saved correctly")
