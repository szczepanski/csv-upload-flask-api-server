# csv upload - flask api server

upload csv file, convert to json and upload to S3 bucket

web access:

http://35.180.79.107/



- [Possible Improvements](#possible-improvements)
  * [Code](#code)
  * [Design](#design)
  * [Security](#security)
  * [Budget](#budget)


# Possible Improvements

## Code 

- more modularity could be introduced by separation of python modules that could separately deal with:

  - aws functions
  - file conversion functions 
  - flask app functions
  - security functions - JWT

- separation of code and variables by introduction of varaibles.yml file that would hold all vars and values. 


## Design 

- improved scalability by adding load ballancing - ELB and auto scaling groups (EC2 based solution)
- utilization of Route 53
- containerization / microservice - docker and possibly K8 for scalability


## Security 

- SSL, TLS / HTTPS instead of http
- Authorization with Flask-JWT - JSON Web Tokens
- introduction of web-facing ELB in dedicated public subnet (connected to AWS - IGW)
- separation and hardening security of VPC's subnets - 3 tier desing (AWS security groups <instance level> and ACL <network level> )
 - I -> public - web facing ELB subnet
 - II -> private - application server hidden behind the ELB
 - III - > private - DB subnet to secure and separate data from   
 
 Gateway Endpoints
- introduction of AWS - KMS and / or Vault cluster


## Budget

- transitioning EC2 based solution to serverless - AWS lamba function solution

## Infrastracture as Code / IaC - Orchestartion

- transisioning the backend AWS infra deployment into IaC design
- 







