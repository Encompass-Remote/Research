
## **Fast Healthcare Interoperability Resources (FHIR)**

### **Data Formats**

FHIR supports both JSON and XML formats for data representation. Each healthcare entity is modeled as a "resource," as elaborate below. 

- **Patient**: represents the individual with the implanted device.

- **Device**: provides details about the CIED like manufacturer, model, and serial number. 

- **Observation**: stores measurements and events reported from the device like heart rate, arrhythmia detections, and battery status.

- **Procedure**: keeps the device-specific implantation or replacement instructions.

- **Encounter**: records interactions between the patient and healthcare providers in relation to the device.

Here’s an example of the JSON format:

    {
     "resourceType": "Observation",
     "id": "example",
     "status": "final",
     "code": {
       "coding": [{
         "system": "http://loinc.org",
         "code": "8867-4",
         "display": "Heart rate"
       }]
     },
     "subject": {
       "reference": "Patient/example"
     },
     "valueQuantity": {
       "value": 72,
       "unit": "beats/minute",
       "system": "http://unitsofmeasure.org",
       "code": "/min"
     }
    }

**Representing Cardiac Device Data**

FHIR provides specialized profiles for cardiac devices. The Cardiovascular Implantable Electronic Device (CIED) profile defines how to represent data from devices like pacemakers and defibrillators. This includes patient information, device identifiers, and observation data. Each resource has a corresponding profile. For example, the CIEDPatient Profile has particular information about the patient resources.

**Profiles vs. Resources**

Why would someone use a profile over the resource?

Each resource has a defined structure (Patient.name, Patient.birthDate) and is meant to be generic and flexible for global healthcare needs, so each resource has optional and required elements. 

A FHIR profile is a customization of a base resource to suit specific clinical, national, or organizational needs. A profile can restrict the base resource (make an optional element required), add rules (enforce that Device.manufacturer must come from a specific data set), add extensions for data not included in the base spec (like battery voltage in a cardiac device), and ensure interoperability between systems exchanging the same kind of data.


### **Potential API Integration**

FHIR supports the traditional GET, POST, PUT, and DELETE HTTP methods along with all response clauses. 

Use FHIR profiles from CardX CIED for specific patient, device, observation, and procedure use-cases.

If the data is already in FHIR, accept POST resources and make sure the meta profile tag matches the correct CardX profile. Otherwise, if the data is HL7 v2, use a transition layer (like mirth connect, smile cdr, or a custom script) to convert HL7 to FHIR.

Then, the data can be validated against CardX CIED profiles using HL7 FHIR Validator CLI, or [Simplifier.net](http://simplifier.net) validator to ensure all required fields are present, enforce value sets, and confirm the profile is in compliance via meta.profile.

All of this data can be stored in a FHIR-compatible format like in a FHIR server or custom SQL/noSQL database with normalized fields and query support.

Next, the API can be built using standard FHIR endpoints like GET /Observatio?patient=123\
This FHIR standard is useful if third parties or new team members look at the project. Other endpoints can be made and tailored to specific needs. Finally, the data can be formatted and security measures can be put into place.


### **Security**

FHIR supports OAuth 2.0 for secure API access, ensuring that only authorized personnel can retrieve or modify patient data.

Additional security is considered best practice. This includes all data exchanges taking place over HTTPS using TLC for encrypted data transits, RBAC so resources are controlled based on user roles, and audit logging so that data access and modifications hold accountability. 


### **Resources**

CardX CIED Implementation Guide:[ https://build.fhir.org/ig/HL7/CardX-CIED/](https://build.fhir.org/ig/HL7/CardX-CIED/)

FHIR Implementation Guide: <https://www.fhir.org/guides/registry/>

FHIR Specifications: <https://www.hl7.org/fhir/>
