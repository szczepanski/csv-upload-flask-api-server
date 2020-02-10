


# csv upload - flask api server

upload csv file, convert to json and upload to S3 bucket

access:

http://35.180.79.107/


# Possible Improvements

## Code 

- more modularity could be introduced- separate python modules that could deal with:

  - aws functions
  - file conversion functions 
  - flask app functions
  - security functions - JWT

- separation of code and variables by introduction of varaibles.yml file that would hold all vars and values. 


## Design 

- improved scalability by adding load ballancing - ELB 
- containerization / microservice - docker and possibly K8 for scalability


## Security 

- SSL, TLS / HTTPS instead of http
- JSON Web Tokens 

## Budget 
AWS lamba function 





