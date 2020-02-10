#!/usr/bin/env python3

"""
csv file upload - flask api server
converts csv file into jsnon and uploads to AWS S3 bucket
"""

__author__ = "Piotr Szczepanski"
__version__ = "0.1.0"
__license__ = "MIT"


import os
import csv, json
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import hashlib

import logging
import boto3
from botocore.exceptions import ClientError


ALLOWED_EXTENSIONS = set(['csv'])

def s3BucketList():
	
	# Retrieve the list of existing buckets
	s3 = boto3.client('s3')
	response = s3.list_buckets()

	# Output the bucket names
	print('Existing buckets:')
	for bucket in response['Buckets']:
	    print(f'  {bucket["Name"]}')
		  
		  
def s3BucketCreate(bucket_name, region):

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True
		  

def s3BucketFileUpload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True		  


def converCsvToList(csv_file_path):
	with open(csv_file_path) as f:
		output_list = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
	
	# convert all numbers to integers
	for item in output_list:
		for key, value in item.items():
			try:
				item[key]=int(value)
			except ValueError:
				item[key] = value
	return output_list


def getFileMd5(csv_file_path):
	hash_md5 = hashlib.md5()
	with open(csv_file_path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

		  
@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')

			csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			json_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cities.json')
						
			
			data = converCsvToList(csv_file_path)
			md5 = getFileMd5(csv_file_path)
			output_json = {'Data': data, 'md5': md5}
			
			with open(json_file_path, 'w') as f:
				json.dump(output_json, f)
			
			s3BucketCreate('the-bla-buckets', 'eu-west-3')
			s3BucketList()
			s3BucketFileUpload_file(json_file_path, 'the-bla-buckets', 'cities.json')

			return output_json

		else:
			flash('The allowed file type is csv. ')
			return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
