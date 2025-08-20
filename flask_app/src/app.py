import os
from flask import Flask, render_template, send_from_directory, abort, jsonify
import json
import csv

app = Flask(__name__)

# Configuration
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
HOTSPOTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json_data')

# Pre-load csv file
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils', 'parts_data.csv'), 'r') as file:
    reader = csv.DictReader(file)
    csv_parts = [row for row in reader]

@app.route('/')
def index():
    """Main route that displays the image gallery."""
    try:
        # Get list of image files from the images folder
        image_files = os.listdir(IMAGES_FOLDER)
        image_files.sort()

        return render_template('index.html', images=image_files)
    except Exception as e:
        return f"Error loading images: {str(e)}", 500

@app.route('/view/<image_id>')
def view_image(image_id):
    """Route to view individual image by ID."""
    try:
        image_filename = f"{image_id}.jpg"
        image_hotspots = get_image_hotspots(image_id)['hotspots']
        formatted_hotspots = []
        # multiply x and y by 1000 to get percentage
        for hotspot in image_hotspots:
            formatted_hotspots.append({
                'id': hotspot['id'],
                'x': float(hotspot['position']['x']) * 800 - 9,
                'y': float(hotspot['position']['y']) * 600 - 9
            })
        return render_template('image_view.html', 
                             image_name=image_filename, 
                             image_id=image_id,
                             image_hotspots=formatted_hotspots)
    except Exception as e:
        return f"Error loading image: {str(e)}", 500

@app.route('/images/<filename>')
def serve_image(filename):
    """Route to serve individual image files."""
    try:
        return send_from_directory(IMAGES_FOLDER, filename)
    except Exception as e:
        return f"Error serving image: {str(e)}", 404


# Helper functions
def get_image_hotspots(image_id):
    with open(os.path.join(HOTSPOTS_FOLDER, f"{image_id}.json"), 'r') as file:
        return json.load(file)



'''
"diagram_id": "5T8NSL2QEJLXGP94EW9Z",
  "image_filename": "5T8NSL2QEJLXGP94EW9Z.jpg",
  "make": "Ferrari",
  "model": "Ferrari GTC4Lusso",
  "sub_model": "Ferrari GTC4Lusso",
  "section": "Plates and Labels",
  "sub_section": "Adhesive Labels And Plaques",
  "hotspots": [
    {
      "hotspot_number": 1,
      "part_number": "12858780",
      "description": "ADHESIVE UNLEADED PETROL/GASOLINE LABEL VIN Check",
      "price_gbp": 2.27,
      "availability": 1,
      "page_url": "https://www.scuderiacarparts.com/part-finder/ferrari/gtc4lusso/oe/340/2606"
    },
   ]
   }

   hotspot_details = {
                    "diagram_id": image_id,
                    "image_filename": image_id + ".jpg",
                    "make": data['Make'],
                    "model": data['Model'],
                    "sub_model": data['Sub-Model'],
                    "section": data['Section Name'],
                    "sub_section": data['Sub-Section Name'],
                    "hotspot_number": hotspot['id'],
                    "part_number": hotspot['parts'][0],
                    "description": hotspot['description'],
                    "price_gbp": hotspot['price_gbp'],
                    "availability": hotspot['availability'],
                    "page_url": hotspot['page_url']
                }
'''

@app.route('/hotspots/<image_id>/<hotspot_id>')
def get_hotspot_data(image_id, hotspot_id):
    with open(os.path.join(HOTSPOTS_FOLDER, f"{image_id}.json"), 'r') as file:
        data = json.load(file)
        hotspots = data['hotspots']
        hotspot = [hotspot for hotspot in hotspots if hotspot['id'] == hotspot_id][0]

        print(hotspot)

        hotspot_details = {
            "label": hotspot_id,
            "parts": []
        }

        # Populate parts in hotspots
        hotspot_parts = []

        for id in hotspot['parts']:
            print(id)
            for data in csv_parts:
                if data['Diagram ID'] == image_id  and data['Part Number'] == id:
                    hotspot_parts.append({
                        "part_number": data['Part Number'],
                        "description": data['Part Description'],
                        "price_gbp": data['Price (GBP)'],
                        "availability": data['Availability'],
                        "page_url": data['Page URL']
                    })

        hotspot_details['parts'] = hotspot_parts

        return jsonify(hotspot_details)


                
                

if __name__ == '__main__':   
    app.run(debug=True, host='0.0.0.0', port=5000)
