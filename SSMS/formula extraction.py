import openpyxl
def extract_formulas(file_path):
    workbook = openpyxl.load_workbook(file_path, data_only=False)
    sheet = workbook.active

    formulas = []
    headers = []
    for row_index, row in enumerate(sheet.iter_rows()):
        if row_index == 0:
            headers = [cell.value for cell in row]
        else:
            for col_index, cell in enumerate(row):
                if cell.data_type == 'f':
                    formulas.append(f"Formula used in {headers[col_index]} ({cell.coordinate}) -> {cell.value}")

    workbook.close()

    return formulas
def main():
    file_path = '/Users/akhilsharma/Desktop/Internship project/Formula_extraction/areaCalculationSheet.xlsx'
    formulas = extract_formulas(file_path)

    if formulas:
        print("List of formulas used in the Excel sheet:")
        for formula in formulas:
            print(formula)
    else:
        print("No formulas found in the Excel sheet.")
if __name__ == "__main__":
    main()