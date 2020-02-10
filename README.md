


# csv upload - flask api server

upload csv file, convert to json and upload to S3 bucket

web access:

http://35.180.79.107/


# Possible Improvements

## Code 

- more modularity could be introduced by separation of python modules that could separately deal with:

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
- Authorization with Flask-JWT - JSON Web Tokens

## Budget

transitioning EC2 based solution to serverless - AWS lamba function solution


