import petl as etl
import csv


def data_integration():
    clinic_location = etl.fromxml('./dataset/clinic_locations.xml', 'Clinic', {
        'ClinicID': 'ClinicID', 'Latitude': 'Lat', 'Longitude': 'Lon'
    })
    clinics = etl.fromcsv('./dataset/clinics.csv')
    clinic_services = etl.fromcsv('./dataset/clinic_services.csv')
    clinics = etl.cut(clinics, 'ClinicID', 'Suburb', 'Postcode')
    clinics_join_clinic_location = etl.outerjoin(clinics, clinic_location, key='ClinicID')
    clinic_services_join_clinics_join_clinic_location = etl.join(clinic_services, clinics_join_clinic_location,
                                                                 key='ClinicID')
    final_data = etl.tocsv(clinic_services_join_clinics_join_clinic_location, './dataset/clinic_service_locations.csv')
