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

def s3List():
	
	# Retrieve the list of existing buckets
	s3 = boto3.client('s3')
	response = s3.list_buckets()

	# Output the bucket names
	print('Existing buckets:')
	for bucket in response['Buckets']:
	    print(f'  {bucket["Name"]}')
	print('No Buckets')
	  
	  

def csvToJson(csv_file_path, json_file_path):
	data = {}

	with open(csv_file_path) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for rows in csv_reader:
			LatD = rows['LatD']
			data[LatD] = rows
	with open(json_file_path, 'w') as json_file:
		json_file.write(json.dumps(data, indent=4))
	
		return json_file


def converCsvToList(csv_file_path):
	with open(csv_file_path) as f:
		a = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
	
	for item in a:
		for key, value in item.items():
			try:
				item[key]=int(value)
			except ValueError:
				item[key] = value
	print(a)
	return a

def getFileMd5(csv_file_path):
	hash_md5 = hashlib.md5()
	with open(csv_file_path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	print(hash_md5.hexdigest())
	return hash_md5.hexdigest()


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

s3List()

		  
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
			json_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'file.json')
			
			# json_file = csvToJson(csv_file_path, json_file_path)
			# print(type(json_file))
			# with open(json_file_path, 'r') as f2:
			# 	data = f2.read()
			# 	print(data)
			# 	return data
			
			data = converCsvToList(csv_file_path)
			md5 = getFileMd5(csv_file_path)
			output_json = {'Data': data, 'md5': md5}
			return output_json

		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
