from yattag import Doc

def generate_xml_from_dataframe(df, company):
    doc, tag, text = Doc().tagtext()

    with tag('ENVELOPE'):
        with tag('HEADER'):
            with tag('TALLYREQUEST'):
                text('Import Data')
        with tag('BODY'):
            with tag('IMPORTDATA'):
                with tag('REQUESTDESC'):
                    with tag('REPORTNAME'):
                        text('Vouchers')
                    with tag('STATICVARIABLES'):
                        with tag('SVCURRENTCOMPANY'):
                            company = company[0:-6]
                            text(company)
                with tag('REQUESTDATA'):
                    for index, row in df.iterrows():
                        with tag('TALLYMESSAGE'):
                            reference = f"{row['Sales_Inv_From']}to{row['Sales_Inv_to']}"
                            with tag('VOUCHER', REMOTEID='3feed323-e41a-4413-970e-e32f83632746-'+reference, VCHTYPE='Sales', ACTION='Create', OBJVIEW='Accounting Voucher View'):
                                with tag('DATE'):
                                    datestr = str(row['BillDate'])[0:10] 
                                    datestr = datestr.replace('-','')
                                    text(datestr)
                                with tag('GUID'):
                                    text('3feed323-e41a-4413-970e-e32f83632746-'+reference)
                                with tag('NARRATION'):
                                    text('Replace with Narration')
                                with tag('VOUCHERTYPENAME'):
                                    text('Sales')
                                with tag('REFERENCE'):
                                    text(reference)
                                with tag('VOUCHERNUMBER'):
                                    text(reference)
                                with tag('PERSISTEDVIEW'):
                                    text('Accounting Voucher View')

                                ledger_entries = [
                                    ("Retail_Customer", -row['Retail_Customer']),
                                    ("Sales @ 5% GST", row['Sales @ 5% GST']),
                                    ("CGST 2.5%", row['CGST 2.5%']),
                                    ("SGST 2.5%", row['SGST 2.5%']),
                                    ("Sales @ 12% GST", row['Sales @ 12% GST']),
                                    ("CGST 6%", row['CGST 6%']),
                                    ("SGST 6%", row['SGST 6%']),
                                    ("Round off", row['Round off'])
                                ]

                                for entry in ledger_entries:
                                    with tag('ALLLEDGERENTRIES.LIST'):
                                        with tag('LEDGERNAME'):
                                            text(entry[0])
                                        with tag('ISDEEMEDPOSITIVE'):
                                            text("Yes" if entry[1] <= 0 else "No")
                                        with tag('REMOVEZEROENTRIES'):
                                            text("No")
                                        with tag('AMOUNT'):
                                            text(entry[1])

    return doc.getvalue()
