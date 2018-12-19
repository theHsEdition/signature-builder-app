#!/usr/bin/env python

# Copyright 2018 Patrick Hanus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import csv
import string

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


## ----------  Handle Uploading multiple Files -- x doesn't work 

from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                self.uploadfile()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


## ----------  Handle Uploaded File -- x doesn't work 
## Ideally, this bit here is where the file is checked to make sure
## it's not bad and then it's assigned the proper variable, based on the file type


def uploadfile(request):

data = {}

if "GET" == request.method:
    return render(request, "myapp/upload_files.html", data)

# if not GET, then proceed
try:
    uploadFile = request.FILES["csv_file1"]
    
    # if file is csv
    if uploadFile.name.endswith('.csv'):
        csv_data_path = uploadFile
    # if file is htm or html
    if uploadFile.name.endswith('.htm', '.html'):
        htm_template_path = uploadFile

    # if the file is not the correct type, regect it.
    else:
        messages.error(request,'File is not CSV or Html type')
        return HttpResponseRedirect(reverse("myapp:upload_files"))

    # if file is too large, return
    if uploadFile.multiple_chunks():
        messages.error(request,"Uploaded file is too big (%.2f MB)." % (uploadFile.size/(1000*1000),))
        return HttpResponseRedirect(reverse("myapp:upload_csv"))

    # Skip empty lines
    file_data = csv_data_path.read().decode("utf-8")
    lines = file_data.split("\n")

    # Use the compile function I wrote
    compile_data( htm_template_path, lines )

except Exception as e:
    logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
    messages.error(request,"Unable to upload file. "+repr(e))

return HttpResponseRedirect(reverse("myapp:upload_csv"))


### ---------- This part works -----------------------
### This is where the processesing happens.



# I want this to be a funtion that is called, passing the values into the function
def compile_data( htm_template_path, csv_data_path ):
    if __name__ == '__main__':

        # Open template file and pass string to 'data'.
        # Will be in HTML format except with the string.Template replace
        # tags with the format of '$var'. The 'var' MUST correspond to the
        # items in the heading row of the input CSV file.
        with open( htm_template_path , 'r') as my_template:
            data = my_template.read()
            # Print template for visual cue.
            print('Template loaded:')
            print(data)
            # Pass 'data' to string.Template object data_template.
            data_template = string.Template(data)

        # Open the input CSV file and pass to dictionary 'input_file'
        with open(csv_data_path,) as csv_file:
            input_file = csv.DictReader(csv_file, delimiter=',')

            for row in input_file:

                    # Create filenames for the output HTML files
                    filename = row['fname'] + row['lname'] + '.htm'
                    # Print filenames for visual cue.
                    print(filename)
                    # Create output HTML file.
                    with open(filename, 'w') as output_file:
                        # Run string.Template substitution on data_template
                        # using data from 'row' as source and write to
                        # 'output_file'.
                        output_file.write(data_template.substitute(row))
        
    # Print the number of files created as a cue program has finished.
    print(str(input_file.line_num - 1) + ' files were created.')        

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'url': '/',
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]

# [START Signature Builder]
class SignatureBuilder(webapp2.RequestHandler):

    def post(self):

        greeting.content = self.request.get('content')
        signature.put()

        query_params = {'signature_builder': signature_builder}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/submit', SignatureBuilder),
], debug=True)
# [END app]
