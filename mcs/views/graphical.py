from django.shortcuts import render
from mcs.models import *

def graphicalAnalysis(request):
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()
	context['DateTime'] = Files.objects.values_list('DateTime', flat=True)

	context['latlong'] = Files.objects.values('lat','lon')
	district = []
	for latlong in context['latlong']:
		district.append(latlongCalc(latlong['lat'],latlong['lon']))
			
	context['latlongFinal'] = dict((x,district.count(x)) for x in set(district))	
	
	
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}
	for listItems in context['Health']:
		if listItems[1] in context['HealthData']:
			context['HealthData'][listItems[1]] = context['HealthData'][listItems[1]] + int(listItems[2])
		else:	
			context['HealthData'][listItems[1]] = listItems[2]

	print context['HealthData']
	
	context['Food'] = Food.objects.values_list()

	context['FoodData'] = {}
	for listItems in context['Food']:
		if listItems[1] in context['FoodData']:
			context['FoodData'][listItems[1]] = context['FoodData'][listItems[1]] + int(listItems[2])
		else:	
			context['FoodData'][listItems[1]] = listItems[2]


	context['Victims'] = Victims.objects.values_list()
	context['VictimsCount'] = Victims.objects.all().count()
	context['VictimData'] = {}
	context['VictimDataPerc'] = {}

	for listItems in context['Victims']:
		if listItems[1] in context['VictimData']:
			context['VictimData'][listItems[1]] = context['VictimData'][listItems[1]] + int(listItems[2])

		else:	
			context['VictimData'][listItems[1]] = listItems[2]
			
	for listItem in context['VictimData'].iteritems():
		context['VictimDataPerc'][listItem[0]] = (listItem[1] * 100/sum(context['VictimData'].values()))
		
	context['years'] = list()
	for years in context['DateTime']:
		val1 = str(years)
		
		context['years'].append(val1[:7])

	if context['countAllFiles'] > 0:
		context['audioDistribution'] = ((context['countAUD'] * 100) /
										context['countAllFiles'])
		context['smsDistribution'] = ((context['countSMS'] * 100) /
									  context['countAllFiles'])
		context['imageDistribution'] = ((context['countIMG'] * 100) /
										context['countAllFiles'])
		context['txtDistribution'] = ((context['countTXT'] * 100) /
									  context['countAllFiles'])
		context['videoDistribution'] = ((context['countVID'] * 100) /
										context['countAllFiles'])

		context['countYears'] = {i:context['years'].count(i) for i in context['years']}
		

	return render(request, 'mcs/graphical.html', context)
def latlongCalc(lati,longi):
	f = open('../offlinemcs/static/map/district.txt','r')
	
	x = f.readline()
	y = x.split(',')
	olat = y[2][2:-3]
	olong = y[3][2:-3]
	minLat = 100
	minLong = 100
	i = 0 
	while i<942:
		x = f.readline()
		y = x.split(',')
		olat = y[2][2:-3]
		olong = y[3][2:-3]

		if((abs(lati - float(olat)) < minLat) and (abs(longi - float(olong)) < minLong)):
			#print 'True:' + str(abs(lati-float(olat))) + '<' + str(minLat)
			#print 'Lat: '+ str(minLat) + 'Long:'+ str(minLong) + 'City:' + city
			minLat = abs(lati - float(olat))
			minLong = abs(longi - float(olong))
			city = y[1].replace("'","")
		i = i + 1
	
	return city
