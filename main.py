import os
import setup_whtmltopdf
import get_file_sz as sz

if __name__ == "__main__":
    if 'wkhtmltopdf' not in os.listdir(r'C:\Program Files'):
        setup_whtmltopdf.setup_pck()
    sz.get_policy_table()