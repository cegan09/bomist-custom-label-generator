# bomist-custom-label-generator
Script for generating custom bomist part labels

BOMIST currently doesn't allow for custom formatted labels within the app, however you can use the API to format them however you want. This script pulls the full list of all your parts, then makes requests for each part to generate a label for each. 

This script is heavily written around the fact that I use custom internal part numbers for all parts in the format used by indaBOM, XXX-XXXX-XX. If you do not use this format for internal part numbers, or do not use internal part numbers, you will need to alter the script in order to work. 

BOMIST uses the following names for sections of the barcode labels:
- barcode: The information encoded in the QR code or data matrix
- title: Top Level Text. Defaults to part number, this script changes to use internal part number
- subtitle: Next line, smaller text. defaults to manufacturer, this script changes to the category label, ie resistor, capacitor, etc.
- meta: Bolded next line, this script sets to manufacturer part number
- description: final lines, default and this script uses the description from the part information

Any of these fields can be changed to any other field from the part data. 

The script renames all files to be named the same as the internal part number, and then moves them into sorted folders that are named the same as the first 3 numbers in the internal part number. Again, this will need to be updated if you do not use this formatting. 


Recommended to use in a python venv environment, will need to install requests library. 
