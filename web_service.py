from bottle import route, run, template, request, error
import petl as etl
import data_integration as di

'''
Queensland Health sample site for searching postcode and services

Functions
def index() -> index page
def allRecord() -> shows all record from integrated dataset
def getServices() -> For searching the services with respect to inputted 'Postcode'
def getClinics() -> For searching the clinics with respect to inputted 'Service'
def loadData() -> creating json data

Variables
data_list => Json data
postcode => inputted postcode data from services.html
service => inputted service data from clinics.html
services => postcode filtered data
clinics => service filtered data
records => set filtered data for accessing from template
'''


@error(404)
def error404(error):
    return '<h1>Page not found. Enter correct url.</h1>'


@error(405)
def error405(error):
    return '<h1>Sorry method not allow. Please review your method once more. <br><span align="center">Thankyou</span></h1>'


@error(500)
def error500(error):
    return '<h1>Something went wrong. Please go to homepage.</h1>'


@route('/')
def index():
    return template('index')


@route('/records', method='GET')
def allRecord():
    return template('allrecord', records=loadData())


@route('/getServices', method='GET')
def getServices():
    postcode = request.params.get('postcode')
    datas = loadData()
    services = list()
    for data in datas:
        if data['Postcode'] == postcode:
            services.append(data)
    return template('services', records=services, postcode=postcode)


@route('/getClinics', method='GET')
def getClinics():
    service = request.params.get('service')
    datas = loadData()
    clinics = list()
    for data in datas:
        if data['Service'] == service:
            clinics.append(data)
    return template('clinics', records=clinics, service=service)


def loadData():
    datacsv = etl.fromcsv('./dataset/clinic_service_locations.csv', )
    datacsv = etl.skip(datacsv, 1)
    data_list = list()
    for data in datacsv:
        data_dict = dict()
        data_dict['ClinicServiceID'] = data[0]
        data_dict['ClinicID'] = data[1]
        data_dict['Service'] = data[2]
        data_dict['Suburb'] = data[3]
        data_dict['Postcode'] = data[4]
        data_dict['Latitude'] = data[5]
        data_dict['Longitude'] = data[6]
        data_list.append(data_dict)
    return data_list


if __name__ == '__main__':
    di.data_integration()
    run(debug=True, reloader=True)
