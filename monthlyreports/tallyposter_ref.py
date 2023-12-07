from openpyxl import load_workbook
from yattag import *
doc, tag, text, line = Doc().ttl()

# wb = load_workbook("demo_database.xlsx")
# ws = wb.worksheets[0]

with tag('ENVELOPE'):
    with tag('HEADER'):
        with tag('TALLYREQUEST'):
            text('Import Data')
    with tag('BODY'):
        with tag('IMPORTDATA'):
            with tag('REQUESTDESC'):
                line('REPORTNAME','Vouchers')
                with tag('STATICVARIABLES'):
                    with tag('SVCURRENTCOMPANY'):
                        text('Test')    #company name to be changed from DB
            with tag('REQUESTDATA'):
                with tag('TALLYMESSAGE', 'xmlns:UDF="TallyUDF"'): # include GUID below
                    with tag("VOUCHER","REMOTEID='3feed323-e41a-4413-970e-e32f83632746-'","VCHTYPE='Sales'", "ACTION='Create'","OBJVIEW='Accounting Voucher View'"):
                        line("DATE","test")
                        line("GUID","3feed323-e41a-4413-970e-e32f83632746-9DN30315/R/22-23") # Replace GUID
                        line("NARRATION","Replace with Narration") # Replace Narration
                        line("VOUCHERTYPENAME","Sales") # Replace with voucher Type
                        line("REFERENCE","9DN30315/R/22-23") # Replace Reference Number
                        line("VOUCHERNUMBER","9DN30315/R/22-23") # Replace Reference Number
                        line("PARTYLEDGERNAME","MADRAS CHIP BOARD LTD")
                        line("PERSISTEDVIEW","Accounting Voucher View")
                        with tag("ALLLEDGERENTRIES.LIST"):
                            line("LEDGERNAME","MADRAS CHIP BOARD LTD") # Replace with party Ledger
                            line("ISDEEMEDPOSITIVE","Yes")
                            line("REMOVEZEROENTRIES","No")
                            line("ISPARTYLEDGER","Yes")
                            line("AMOUNT","-2448") # Replace with amount
                            with tag("BILLALLOCATIONS.LIST"):
                                line("NAME","9DN30315/R/22-23") # change with Bill Number
                                line("BILLTYPE","New Ref")
                                line("AMOUNT","-2448") # Replace with amount
                        with tag("ALLLEDGERENTRIES.LIST"):
                            line("LEDGERNAME","Sales Ledger") # Replace with sales Ledger
                            line("ISDEEMEDPOSITIVE","No")
                            line("REMOVEZEROENTRIES","No")
                            line("AMOUNT","2448") # Replace with amount
                            with tag("CATEGORYALLOCATIONS.LIST"):
                                line("CATEGORY","TELECOM & RTA") # change Cost Center
                                line("REMOVEZEROENTRIES","No")
                                with tag("COSTCENTREALLOCATIONS.LIST"):
                                    line("NAME","RTA") # Change with cost center Name
                                    line("AMOUNT","2448") # Replace with amount

result = indent(doc.getvalue())
# print (result)
with open("output.xml","w") as f:
    f.write(result)