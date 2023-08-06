import os
from openpyxl import load_workbook

# List of Columns with categorical variables
LST_CATG_VARIABLES = ['location', 'billing_provider', 'proc_code', 'pos_type', 'pos_group']


####################################################################################
##  Postgres Database Credentials
####################################################################################

# Development Server
PG_DEV_PASS = os.environ['PG_DEV_PASS']
PG_DEV_USER = os.environ['PG_DEV_USER']
PG_DEV_HOST = os.environ['PG_DEV_HOST']
PG_DEV_PORT = os.environ['PG_DEV_PORT']
PG_DEV_DB = os.environ['PG_DEV_DB']

# Production Server
PG_PROD_PASS = os.environ['PG_PROD_PASS']
PG_PROD_USER = os.environ['PG_PROD_USER']
PG_PROD_HOST = os.environ['PG_PROD_HOST']
PG_PROD_PORT = os.environ['PG_PROD_PORT']
PG_PROD_DB = os.environ['PG_PROD_DB']


####################################################################################
##  Oracle Database Credentials
####################################################################################

data_source_file_oracle = "\\\\hsc-evs03.ad.utah.edu\\users\\" + os.getlogin() + "\\Data Sources\\UIDPWD.xlsx"
wb_credentials_oracle = load_workbook(data_source_file_oracle)
sheet_oracle = wb_credentials_oracle['Sheet1']
ORACLE_USER = sheet_oracle['A2'].value
ORACLE_PASS = sheet_oracle['B2'].value