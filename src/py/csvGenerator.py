# coding=utf-8
import json
import csv
import unicodedata

with open('waterData.json') as f:
	data = json.load(f)
#print(data["Afghanistan"]["Municipal water withdrawal as % of total withdrawal"]["2000"])
isoDic = {
	"Afghanistan":"AFG",
	"Albania":"ALB",
	"Algeria":"DZA",
	"Andorra":"AND",
	"Angola":"AGO",
	"Antigua and Barbuda":"ATG",
	"Argentina":"ARG",
	"Armenia":"ARM",
	"Australia":"AUS",
	"Austria":"AUT",
	"Azerbaijan":"AZE",
	"Bahamas":"BHS",
	"Bahrain":"BHR",
	"Bangladesh":"BGD",
	"Barbados":"BRB",
	"Belarus":"BLR",
	"Belgium":"BEL",
	"Belize":"BLZ",
	"Benin":"BEN",
	"Bhutan":"BTN",
	"Bolivia (Plurinational State of)":"BOL",
	"Bosnia and Herzegovina":"BIH",
	"Botswana":"BWA",
	"Brazil":"BRA",
	"Brunei Darussalam":"BRN",
	"Bulgaria":"BGR",
	"Burkina Faso":"BFA",
	"Burundi":"BDI",
	"Cabo Verde":"CPV",
	"Cambodia":"KHM",
	"Cameroon":"CMR",
	"Canada":"CAN",
	"Central African Republic":"CAF",
	"Chad":"TCD",
	"Chile":"CHL",
	"China":"CHN",
	"Colombia":"COL",
	"Comoros":"COM",
	"Congo":"COG",
	"Cook Islands":"COK",
	"Costa Rica":"CRI",
	"Croatia":"HRV",
	"Cuba":"CUB",
	"Cyprus":"CYP",
	"Czechia":"Czechia",
	"Côte d'Ivoire":"CIV",
	"Democratic People's Republic of Korea":"PRK",
	"Democratic Republic of the Congo":"COD",
	"Denmark":"DNK",
	"Djibouti":"DJI",
	"Dominica":"DMA",
	"Dominican Republic":"DOM",
	"Ecuador":"ECU",
	"Egypt":"EGY",
	"El Salvador":"SLV",
	"Equatorial Guinea":"GNQ",
	"Eritrea":"ERI",
	"Estonia":"EST",
	"Eswatini":"SWZ",
	"Ethiopia":"ETH",
	"Faroe Islands":"FRO",
	"Fiji":"FJI",
	"Finland":"FIN",
	"France":"FRA",
	"Gabon":"GAB",
	"Gambia":"GMB",
	"Georgia":"GEO",
	"Germany":"DEU",
	"Ghana":"GHA",
	"Greece":"GRC",
	"Grenada":"GRD",
	"Guatemala":"GTM",
	"Guinea":"GIN",
	"Guinea-Bissau":"GNB",
	"Guyana":"GUY",
	"Haiti":"HTI",
	"Holy See":"VAT",
	"Honduras":"HND",
	"Hungary":"HUN",
	"Iceland":"ISL",
	"India":"IND",
	"Indonesia":"IDN",
	"Iran (Islamic Republic of)":"IRN",
	"Iraq":"IRQ",
	"Ireland":"IRL",
	"Israel":"ISR",
	"Italy":"ITA",
	"Jamaica":"JAM",
	"Japan":"JPN",
	"Jordan":"JOR",
	"Kazakhstan":"KAZ",
	"Kenya":"KEN",
	"Kiribati":"KIR",
	"Kuwait":"KWT",
	"Kyrgyzstan":"KGZ",
	"Lao People's Democratic Republic":"LAO",
	"Latvia":"LVA",
	"Lebanon":"LBN",
	"Lesotho":"LSO",
	"Liberia":"LBR",
	"Libya":"LBY",
	"Liechtenstein":"LIE",
	"Lithuania":"LTU",
	"Luxembourg":"LUX",
	"Madagascar":"MDG",
	"Malawi":"MWI",
	"Malaysia":"MYS",
	"Maldives":"MDV",
	"Mali":"MLI",
	"Malta":"MLT",
	"Marshall Islands":"MHL",
	"Mauritania":"MRT",
	"Mauritius":"MUS",
	"Mexico":"MEX",
	"Micronesia (Federated States of)":"FSM",
	"Monaco":"MCO",
	"Mongolia":"MNG",
	"Montenegro":"MNE",
	"Morocco":"MAR",
	"Mozambique":"MOZ",
	"Myanmar":"MMR",
	"Namibia":"NAM",
	"Nauru":"NRU",
	"Nepal":"NPL",
	"Netherlands":"NLD",
	"New Zealand":"NZL",
	"Nicaragua":"NIC",
	"Niger":"NER",
	"Nigeria":"NGA",
	"Niue":"NIU",
	"North Macedonia":"MKD",
	"Norway":"NOR",
	"Oman":"OMN",
	"Pakistan":"PAK",
	"Palau":"PLW",
	"Palestine":"PSE",
	"Panama":"PAN",
	"Papua New Guinea":"PNG",
	"Paraguay":"PRY",
	"Peru":"PER",
	"Philippines":"PHL",
	"Poland":"POL",
	"Portugal":"PRT",
	"Puerto Rico":"PRI",
	"Qatar":"QAT",
	"Republic of Korea":"KOR",
	"Republic of Moldova":"MDA",
	"Romania":"ROU",
	"Russian Federation":"RUS",
	"Rwanda":"RWA",
	"Saint Kitts and Nevis":"KNA",
	"Saint Lucia":"LCA",
	"Saint Vincent and the Grenadines":"VCT",
	"Samoa":"WSM",
	"San Marino":"SMR",
	"Sao Tome and Principe":"STP",
	"Saudi Arabia":"SAU",
	"Senegal":"SEN",
	"Serbia":"SRB",
	"Seychelles":"SYC",
	"Sierra Leone":"SLE",
	"Singapore":"SGP",
	"Slovakia":"SVK",
	"Slovenia":"SVN",
	"Solomon Islands":"SLB",
	"Somalia":"SOM",
	"South Africa":"ZAF",
	"South Sudan":"SSD",
	"Spain":"ESP",
	"Sri Lanka":"LKA",
	"Sudan":"SDN",
	"Suriname":"SUR",
	"Sweden":"SWE",
	"Switzerland":"CHE",
	"Syrian Arab Republic":"SYR",
	"Tajikistan":"TJK",
	"Thailand":"THA",
	"Timor-Leste":"TLS",
	"Togo":"TGO",
	"Tokelau":"TKL",
	"Tonga":"TON",
	"Trinidad and Tobago":"TTO",
	"Tunisia":"TUN",
	"Turkey":"TUR",
	"Turkmenistan":"TKM",
	"Tuvalu":"TUV",
	"Uganda":"UGA",
	"Ukraine":"UKR",
	"United Arab Emirates":"ARE",
	"United Kingdom":"GBR",
	"United Republic of Tanzania":"TZA",
	"United States of America":"USA",
	"Uruguay":"URY",
	"Uzbekistan":"UZB",
	"Vanuatu":"VUT",
	"Venezuela (Bolivarian Republic of)":"VEN",
	"Viet Nam":"VNM",
	"Yemen":"YEM",
	"Zambia":"ZMB",
	"Zimbabwe":"ZWE"
}

print(len(dict.keys(isoDic)))

varAttributes = [
"Total area of the country (excl. coastal waters)",
"Total population",
"Surface water produced internally",
"Groundwater produced internally",
"Total internal renewable water resources (IRWR)",
"Total internal renewable water resources per capita",
"Surface water: entering the country (total)",
"Surface water: inflow not submitted to treaties",
"Surface water: inflow submitted to treaties",
"Surface water: inflow secured through treaties",
"Surface water: total flow of border rivers",
"Surface water: accounted flow of border rivers",
"Surface water: accounted inflow",
"Surface water: leaving the country to other countries (total)",
"Surface water: outflow to other countries not submitted to treaties",
"Surface water: outflow to other countries submitted to treaties",
"Surface water: outflow to other countries secured through treaties",
"Surface water: total external renewable",
"Groundwater: entering the country (total)",
"Groundwater: accounted inflow",
"Groundwater: leaving the country to other countries (total)",
"Groundwater: accounted outflow to other countries",
"Water resources: total external renewable",
"Total renewable surface water",
"Total renewable groundwater",
"Total renewable water resources",
"Dependency ratio",
"Total renewable water resources per capita",
"Agricultural water withdrawal",
"Industrial water withdrawal",
"Municipal water withdrawal",
"Total water withdrawal",
"Irrigation water withdrawal",
"Irrigation water requirement",
"Agricultural water withdrawal as % of total water withdrawal",
"Industrial water withdrawal as % of total water withdrawal",
"Municipal water withdrawal as % of total withdrawal",
"Total water withdrawal per capita",
"Fresh surface water withdrawal",
"Fresh groundwater withdrawal",
"Total freshwater withdrawal"]

outputFileNames = [
"Total_area_of_the_country",
"Total_population",
"Surface_water_produced_internally",
"Groundwater_produced_internally",
"Total_internal_renewable_water_resources",
"Total_internal_renewable_water_resources_per_capita",
"Surface_water_entering_the_country",
"Surface_water_inflow_not_submitted_to_treaties",
"Surface_water_inflow_submitted_to_treaties",
"Surface_water_inflow_secured_through_treaties",
"Surface_water_total_flow_of_border_rivers",
"Surface_water_accounted_flow_of_border_rivers",
"Surface_water_accounted_inflow",
"Surface_water_leaving_the_country_to_other_countries_",
"Surface_water_outflow_to_other_countries_not_submitted_to_treaties",
"Surface_water_outflow_to_other_countries_submitted_to_treaties",
"Surface_water_outflow_to_other_countries_secured_through_treaties",
"Surface_water_total_external_renewable",
"Groundwater_entering_the_country",
"Groundwater_accounted_inflow",
"Groundwater_leaving_the_country_to_other_countries",
"Groundwater_accounted_outflow_to_other_countries",
"Water_resources_total_external_renewable",
"Total_renewable_surface_water",
"Total_renewable_groundwater",
"Total_renewable_water_resources",
"Dependency_ratio",
"Total_renewable_water_resources_per_capita",
"Agricultural_water_withdrawal",
"Industrial_water_withdrawal",
"Municipal_water_withdrawal",
"Total_water_withdrawal",
"Irrigation_water_withdrawal",
"Irrigation_water_requirement",
"Agricultural_water_withdrawal_as_percent_of_total_water_withdrawal",
"Industrial_water_withdrawal_as_percent_of_total_water_withdrawal",
"Municipal_water_withdrawal_as_percent_of_total_withdrawal",
"Total_water_withdrawal_per_capita",
"Fresh_surface_water_withdrawal",
"Fresh_groundwater_withdrawal",
"Total_freshwater_withdrawal"]

yearList = [1970,1975,1980,1985,1990,1995,2000,2005,2010,2015]

for v in range(len(varAttributes)):
	var = varAttributes[v]
	content = ""#"country,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015"
	for countryName in dict.keys(data):
		lineToAdd = countryName + ","
		yearData = [None, None, None, None, None, None, None, None, None, None]
		realYear = [None, None, None, None, None, None, None, None, None, None]
		if not data[countryName].has_key(var):
			continue
		for currYear in dict.keys(data[countryName][var]):
			diffFunction = lambda list_value : abs(list_value - int(currYear))
			closestYear = min(yearList, key=diffFunction)
			if closestYear == 1970:
				yearData[0] = "1970"
				realYear[0] = currYear
			elif closestYear == 1975:
				yearData[1] = "1975"
				realYear[1] = currYear
			elif closestYear == 1980:
				yearData[2] = "1980"
				realYear[2] = currYear
			elif closestYear == 1985:
				yearData[3] = "1985"
				realYear[3] = currYear
			elif closestYear == 1990:
				yearData[4] = "1990"
				realYear[4] = currYear
			elif closestYear == 1995:
				yearData[5] = "1995"
				realYear[5] = currYear
			elif closestYear == 2000:
				yearData[6] = "2000"
				realYear[6] = currYear
			elif closestYear == 2005:
				yearData[7] = "2005"
				realYear[7] = currYear
			elif closestYear == 2010:
				yearData[8] = "2010"
				realYear[8] = currYear
			elif closestYear == 2015:
				yearData[9] = "2015"
				realYear[9] = currYear
		for i in range(len(yearData)):
			if yearData[i] == None:
				lineToAdd += ","
			else:
				lineToAdd += str(data[countryName][var][realYear[i]]) + ","
		content += lineToAdd + "\n"
	with open(outputFileNames[v] + ".csv", mode='w') as csv_file:
		fieldNames = ["country","1970","1975","1980","1985","1990","1995","2000","2005","2010","2015","iso3"]
		writer = csv.DictWriter(csv_file, fieldnames=fieldNames)

		writer.writeheader()
		content = u''.join((content)).encode('utf-8')
		lines = content.split("\n")
		#print(outputFileNames[v])
		for line in lines:
			#print(line)
			if(line == ""):
				continue
			cols = line.split(",")
			writer.writerow({"country": cols[0], "1970": cols[1], "1975": cols[2], "1980": cols[3], "1985": cols[4], 
				"1990": cols[5], "1995": cols[6], "2000": cols[7], "2005": cols[8], "2010": cols[9], "2015": cols[10],
				"iso3":isoDic[cols[0]]})
	#print(content)
	#print("\n\n")
print("success")


























