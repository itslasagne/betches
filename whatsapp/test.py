from tika import parser

url = 'https://api.twilio.com/2010-04-01/Accounts/AC8e056bf41d4cc405b996d3cabdd86b67/Messages/MM96bacd499f846d1cfe6e4578b9043d5e/Media/ME581ba06b0bf07e985008732097c034ed'

pdfFile = parser.from_file(url)

print(pdfFile["content"])