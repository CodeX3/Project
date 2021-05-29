import convertapi
convertapi.api_secret = 'bFLSIvtqzK67nYnL'
convertapi.convert('pdf', {
    'File': 'C:\\Users\\ajith\\PycharmProjects\\Project\\HostelManagement\\report\\20210529200447.xlsx'
}, from_format = 'xls').save_files('C:\\Users\\ajith\\PycharmProjects\\Project\\HostelManagement\\report\\')