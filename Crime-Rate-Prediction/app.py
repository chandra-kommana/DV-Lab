from flask import Flask, request, render_template, jsonify
import pickle 
import math
import json
from datetime import datetime
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import folium
from folium import plugins
import os

model = pickle.load(open('Model/model.pkl', 'rb'))

app = Flask(__name__)


city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore',
    '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore',
    '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata',
    '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur',
    '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC',
    '2': 'Crime against ST', '3': 'Crime against Senior Citizen',
    '4': 'Crime against children', '5': 'Crime against women',
    '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
}

population = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10,
    '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20,
    '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10,
    '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

# City Coordinates for Map Visualization
city_coords = {
    'Ahmedabad': [23.0225, 72.5714],
    'Bengaluru': [12.9716, 77.5946],
    'Chennai': [13.0827, 80.2707],
    'Coimbatore': [11.0081, 76.9558],
    'Delhi': [28.7041, 77.1025],
    'Ghaziabad': [28.6692, 77.4538],
    'Hyderabad': [17.3850, 78.4867],
    'Indore': [22.7196, 75.8577],
    'Jaipur': [26.9124, 75.7873],
    'Kanpur': [26.4499, 80.3319],
    'Kochi': [9.9312, 76.2673],
    'Kolkata': [22.5726, 88.3639],
    'Kozhikode': [11.2588, 75.7804],
    'Lucknow': [26.8467, 80.9462],
    'Mumbai': [19.0760, 72.8777],
    'Nagpur': [21.1458, 79.0882],
    'Patna': [25.5941, 85.1376],
    'Pune': [18.5204, 73.8567],
    'Surat': [21.1702, 72.8311]
}

# Emergency Contacts for Cities
emergency_contacts = {
    'Mumbai': {
        'police': '100 / 22889999',
        'women_helpline': '1091',
        'cyber_cell': '9867443555',
        'medical': '102'
    },
    'Delhi': {
        'police': '100 / 23866666',
        'women_helpline': '1091',
        'cyber_cell': '011-24369141',
        'medical': '102'
    },
    'Bengaluru': {
        'police': '100 / 9886960099',
        'women_helpline': '1091',
        'cyber_cell': '080-22942038',
        'medical': '102'
    },
    'Kolkata': {
        'police': '100 / 2214-3400',
        'women_helpline': '1091',
        'cyber_cell': '033-2485-0123',
        'medical': '102'
    },
    'Chennai': {
        'police': '100 / 4429-8888',
        'women_helpline': '1091',
        'cyber_cell': '044-24821777',
        'medical': '102'
    },
    'Hyderabad': {
        'police': '100 / 9911008100',
        'women_helpline': '1091',
        'cyber_cell': '040-23456789',
        'medical': '102'
    },
    'Pune': {
        'police': '100 / 20263333',
        'women_helpline': '1091',
        'cyber_cell': '020-26128888',
        'medical': '102'
    },
    'Ahmedabad': {
        'police': '100 / 6353633',
        'women_helpline': '1091',
        'cyber_cell': '079-40000900',
        'medical': '102'
    },
    'Jaipur': {
        'police': '100 / 5102100',
        'women_helpline': '1091',
        'cyber_cell': '0141-5109100',
        'medical': '102'
    },
    'Lucknow': {
        'police': '100 / 2288-3111',
        'women_helpline': '1091',
        'cyber_cell': '0522-3244622',
        'medical': '102'
    },
    'Kanpur': {
        'police': '100 / 2619-2624',
        'women_helpline': '1091',
        'cyber_cell': '0512-2619100',
        'medical': '102'
    },
    'Nagpur': {
        'police': '100 / 7117-100',
        'women_helpline': '1091',
        'cyber_cell': '0712-2677900',
        'medical': '102'
    },
    'Ghaziabad': {
        'police': '100 / 1171-100',
        'women_helpline': '1091',
        'cyber_cell': '0120-2770444',
        'medical': '102'
    },
    'Indore': {
        'police': '100 / 0731-2525070',
        'women_helpline': '1091',
        'cyber_cell': '0731-2525080',
        'medical': '102'
    },
    'Surat': {
        'police': '100 / 2610-0100',
        'women_helpline': '1091',
        'cyber_cell': '0261-2410100',
        'medical': '102'
    },
    'Kochi': {
        'police': '100 / 4869-9999',
        'women_helpline': '1091',
        'cyber_cell': '0484-2368999',
        'medical': '102'
    },
    'Coimbatore': {
        'police': '100 / 0422-3099400',
        'women_helpline': '1091',
        'cyber_cell': '0422-2563100',
        'medical': '102'
    },
    'Kozhikode': {
        'police': '100 / 0495-2361000',
        'women_helpline': '1091',
        'cyber_cell': '0495-2361100',
        'medical': '102'
    },
    'Patna': {
        'police': '100 / 2232-3456',
        'women_helpline': '1091',
        'cyber_cell': '0612-2232100',
        'medical': '102'
    }
}

# Safety Tips by Crime Type
safety_tips = {
    '6': {  # Cyber Crimes
        'tips': [
            '🔐 Do not share OTPs or passwords with anyone',
            '🔓 Enable two-factor authentication (2FA) on all accounts',
            '🔗 Always check for HTTPS in the URL before entering sensitive information',
            '📧 Do not click links from unknown emails or messages',
            '🛡️ Use antivirus software and keep it updated',
            '⚠️ Be cautious of phishing attempts and fake websites',
            '📱 Do not use public WiFi for banking or shopping',
            '💳 Monitor your bank statements regularly for suspicious activities'
        ]
    },
    '5': {  # Crime against women
        'tips': [
            '🚨 Know the emergency number: 100 / Women Helpline: 1091',
            '📍 Share your location with trusted friends when traveling alone',
            '🤝 Stay with groups, especially during late hours',
            '📱 Keep your phone charged and accessible',
            '🚕 Use verified taxi/ride-sharing services',
            '👥 Inform someone you trust about your whereabouts',
            '💪 Take self-defense classes',
            '🎧 Avoid using headphones while traveling'
        ]
    },
    '4': {  # Crime against children
        'tips': [
            '👶 Monitor children\'s online activities',
            '📱 Keep children\'s location tracked using apps',
            '🚸 Teach children about personal safety',
            '⚠️ Be cautious about strangers approaching children',
            '🏠 Ensure safe transportation to school',
            '💬 Maintain open communication with children',
            '📍 Know the places your children frequently visit',
            '🎓 Educate about online safety and stranger danger'
        ]
    },
    '7': {  # Economic Offences
        'tips': [
            '🏦 Verify any financial offers independently',
            '📄 Always read terms and conditions carefully',
            '💰 Avoid sharing financial details via email or phone',
            '📋 Maintain proper documentation of transactions',
            '🔍 Verify business registration before investing',
            '⚠️ Be wary of "get rich quick" schemes',
            '📧 Never respond to unsolicited investment offers',
            '🏛️ Report suspicious activities to relevant authorities'
        ]
    },
    '8': {  # Kidnapping
        'tips': [
            '🚗 Vary your daily routines and travel routes',
            '📍 Always inform someone about your destination',
            '🔒 Keep car doors locked while traveling',
            '⚠️ Be aware of your surroundings',
            '📱 Keep emergency contacts readily available',
            '👀 Report suspicious behavior to authorities',
            '🏠 Install security systems at home',
            '🚨 Contact police immediately if threatened'
        ]
    },
    '9': {  # Murder
        'tips': [
            '🔒 Install security measures at your residence',
            '⚠️ Be cautious of strangers and unknown contacts',
            '🚨 Report any threats immediately to police',
            '📍 Vary your daily routines',
            '🤝 Maintain good relationships with neighbors',
            '📱 Keep emergency numbers readily available',
            '🏠 Ensure proper lighting around your home',
            '👥 Avoid isolated places, especially during nights'
        ]
    },
    '0': {  # Crime Committed by Juveniles
        'tips': [
            '🎓 Mentor and guide youth in your community',
            '📚 Support educational initiatives for underprivileged youth',
            '🤝 Promote positive peer influence',
            '💬 Keep communication channels open with young people',
            '🎯 Encourage sports and recreational activities',
            '👨‍👩‍👧‍👦 Strengthen family bonds and support systems',
            '⚠️ Report any criminal activity involving minors',
            '🌟 Support rehabilitation programs for juvenile offenders'
        ]
    },
    '3': {  # Crime against Senior Citizen
        'tips': [
            '👴 Check on elderly relatives regularly',
            '💰 Be cautious about financial advice to seniors',
            '📱 Help seniors recognize phone and online scams',
            '📋 Keep proper documentation of property and finances',
            '👥 Ensure senior citizens are not isolated',
            '🏥 Assist with medical and legal matters',
            '⚠️ Report any abuse or neglect immediately',
            '🏠 Ensure a safe and secure living environment'
        ]
    },
    '1': {  # Crime against SC
        'tips': [
            '⚖️ Know your constitutional rights',
            '📋 Document any discrimination or harassment',
            '🤝 Report incidents to relevant authorities',
            '💬 Seek support from community organizations',
            '📞 Contact civil rights organizations for help',
            '👥 Build community support networks',
            '🎓 Pursue education and skill development',
            '🛡️ Know your legal recourse and available resources'
        ]
    },
    '2': {  # Crime against ST
        'tips': [
            '⚖️ Know your constitutional rights and protections',
            '📋 Keep records of land and property documents',
            '🤝 Join community support groups',
            '📞 Contact tribal welfare organizations',
            '💬 Report exploitation to authorities',
            '👥 Maintain unity within the community',
            '🎓 Encourage education and awareness',
            '🛡️ Seek legal help from pro bono legal services'
        ]
    }
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_trend_predictions(year, city_code, crime_code, pop):
    """Generate crime rate predictions for the next 5 years"""
    trends = []
    base_year = int(year)
    city_code_int = int(city_code)
    crime_code_int = int(crime_code)
    base_pop = pop  # Store the population for the initial year
    base_year_for_pop = base_year
    
    for i in range(5):
        current_year = base_year + i
        year_diff = current_year - 2011
        # Calculate population for this specific year using compound growth
        adjusted_pop = base_pop * ((1.01) ** (current_year - base_year_for_pop))
        predicted_rate = model.predict([[current_year, city_code_int, adjusted_pop, crime_code_int]])[0]
        trends.append({
            'year': current_year,
            'rate': round(predicted_rate, 2)
        })
    
    return trends

def create_map(city_name, crime_rate, crime_status):
    """Create an interactive map with city markers"""
    # Center map on India
    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Determine color based on crime rate
    if crime_rate <= 1:
        color = 'green'
        icon_name = 'check'
    elif crime_rate <= 5:
        color = 'yellow'
        icon_name = 'info-sign'
    elif crime_rate <= 15:
        color = 'orange'
        icon_name = 'warning-sign'
    else:
        color = 'red'
        icon_name = 'exclamation-sign'
    
    # Add marker for selected city
    if city_name in city_coords:
        coords = city_coords[city_name]
        folium.Marker(
            location=coords,
            popup=f'{city_name}<br>{crime_status}',
            tooltip=crime_status,
            icon=folium.Icon(color=color, icon=icon_name, prefix='glyphicon')
        ).add_to(m)
        
        # Center map on selected city
        m.location = coords
        m.zoom_start = 8
    
    # Save map to HTML string
    map_html = m._repr_html_()
    return map_html

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    city_code = request.form["city"]
    crime_code = request.form['crime']
    year = request.form['year']
    
    # Convert to integers
    city_code = int(city_code)
    crime_code = int(crime_code)
    year = int(year)
    
    base_pop = population[str(city_code)]

    # Calculate adjusted population using compound growth (1% annually from 2011)
    year_diff = year - 2011
    pop = base_pop * ((1.01) ** year_diff)

    # Get single year prediction
    crime_rate = model.predict([[year, city_code, pop, crime_code]])[0]

    city_name = city_names[str(city_code)]
    crime_type = crimes_names[str(crime_code)]

    # Determine crime status
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area"

    cases = math.ceil(crime_rate * pop)

    # Get trend predictions
    trends = get_trend_predictions(year, city_code, crime_code, pop)

    # Get map
    map_html = create_map(city_name, crime_rate, crime_status)

    # Get emergency contacts
    emergency = emergency_contacts.get(city_name, {})

    # Get safety tips
    tips = safety_tips.get(str(crime_code), {}).get('tips', [])

    return render_template(
        'result.html',
        city_name=city_name,
        crime_type=crime_type,
        year=year,
        crime_status=crime_status,
        crime_rate=round(crime_rate, 2),
        cases=cases,
        population=round(pop, 2),
        trends=json.dumps(trends),
        map_html=map_html,
        emergency=emergency,
        tips=tips,
        city_code=city_code,
        crime_code=crime_code
    )

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF report of prediction"""
    data = request.json

    # Create PDF
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=30,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Title
    elements.append(Paragraph("Crime Rate Prediction Report", title_style))
    elements.append(Spacer(1, 0.3*inch))

    # Main Prediction Data
    elements.append(Paragraph("Prediction Details", heading_style))
    
    prediction_data = [
        ['City', data['city_name']],
        ['Crime Type', data['crime_type']],
        ['Year', data['year']],
        ['Crime Status', data['crime_status']],
        ['Crime Rate', f"{data['crime_rate']} per lakh population"],
        ['Estimated Cases', str(data['cases'])],
        ['Population', f"{data['population']} lakhs"]
    ]

    prediction_table = Table(prediction_data, colWidths=[2*inch, 3.5*inch])
    prediction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))

    elements.append(prediction_table)
    elements.append(Spacer(1, 0.3*inch))

    # Report Footer
    elements.append(Spacer(1, 0.2*inch))
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>Crime Rate Prediction System"
    elements.append(Paragraph(footer_text, styles['Normal']))

    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue(), 200, {
        'Content-Disposition': 'attachment; filename="crime_report.pdf"',
        'Content-Type': 'application/pdf'
    }

@app.route('/get-news/<city_name>', methods=['GET'])
def get_news(city_name):
    """Fetch crime news for the selected city"""
    try:
        api_key = 'YOUR_NEWS_API_KEY'  # Replace with actual API key
        url = f'https://newsapi.org/v2/everything?q={city_name} crime&language=en&sortBy=publishedAt&pageSize=5'
        
        # Note: Without a valid API key, this will return an empty list
        # Users should add their own API key from https://newsapi.org/
        
        headers = {'X-Api-Key': api_key}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return jsonify({
                'success': True,
                'articles': articles[:5]
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not fetch news at this time'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/compare', methods=['POST'])
def compare_cities():
    """Relocation Decision Engine - Compare two cities for safety"""
    city1_code = request.form.get("city1")
    city2_code = request.form.get("city2")
    crime_code = request.form.get("crime")
    year = request.form.get("year", "2024")
    
    # Convert to integers
    city1_code = int(city1_code)
    city2_code = int(city2_code)
    crime_code = int(crime_code)
    year = int(year)
    
    city1_name = city_names.get(str(city1_code), "Unknown")
    city2_name = city_names.get(str(city2_code), "Unknown")
    crime_type = crimes_names.get(str(crime_code), "Unknown")
    
    base_pop1 = population[str(city1_code)]
    base_pop2 = population[str(city2_code)]
    
    # Calculate adjusted population using compound growth
    year_diff = year - 2011
    pop1_adjusted = base_pop1 * ((1.01) ** year_diff)
    pop2_adjusted = base_pop2 * ((1.01) ** year_diff)
    
    # Get predictions for both cities across all crime types
    crime1_rate = model.predict([[year, city1_code, pop1_adjusted, crime_code]])[0]
    crime2_rate = model.predict([[year, city2_code, pop2_adjusted, crime_code]])[0]
    
    # Calculate percentage difference
    if crime1_rate == 0:
        percent_change = -100 if crime2_rate == 0 else float('inf')
    else:
        percent_change = ((crime2_rate - crime1_rate) / crime1_rate) * 100
    
    # Determine if moving is safer
    is_safer = crime2_rate < crime1_rate
    improvement = abs(crime1_rate - crime2_rate)
    
    # Get crime status for both
    def get_status(rate):
        if rate <= 1:
            return "Very Low Crime Area"
        elif rate <= 5:
            return "Low Crime Area"
        elif rate <= 15:
            return "High Crime Area"
        else:
            return "Very High Crime Area"
    
    city1_status = get_status(crime1_rate)
    city2_status = get_status(crime2_rate)
    
    # Calculate comparative metrics across all crime types
    all_crimes_comparison = []
    for crime_id in crimes_names.keys():
        crime_id_int = int(crime_id)
        rate1 = model.predict([[year, city1_code, pop1_adjusted, crime_id_int]])[0]
        rate2 = model.predict([[year, city2_code, pop2_adjusted, crime_id_int]])[0]
        
        change = ((rate2 - rate1) / rate1 * 100) if rate1 != 0 else -100
        all_crimes_comparison.append({
            'crime': crimes_names[crime_id],
            'city1_rate': round(rate1, 2),
            'city2_rate': round(rate2, 2),
            'change': round(change, 2),
            'safer_in': city2_name if rate2 < rate1 else city1_name
        })
    
    # Calculate overall safety score (lower is safer)
    avg_crime1 = sum([model.predict([[year, city1_code, pop1_adjusted, int(cid)]])[0] 
                      for cid in crimes_names.keys()]) / len(crimes_names)
    avg_crime2 = sum([model.predict([[year, city2_code, pop2_adjusted, int(cid)]])[0] 
                      for cid in crimes_names.keys()]) / len(crimes_names)
    
    overall_safer = city2_name if avg_crime2 < avg_crime1 else city1_name
    overall_percent = abs((avg_crime2 - avg_crime1) / avg_crime1 * 100) if avg_crime1 != 0 else 0
    
    return render_template(
        'comparison.html',
        city1_name=city1_name,
        city2_name=city2_name,
        crime_type=crime_type,
        year=year,
        crime1_rate=round(crime1_rate, 2),
        crime2_rate=round(crime2_rate, 2),
        city1_status=city1_status,
        city2_status=city2_status,
        percent_change=round(percent_change, 2),
        improvement=round(improvement, 2),
        is_safer=is_safer,
        all_crimes=all_crimes_comparison,
        overall_safer=overall_safer,
        overall_percent=round(overall_percent, 2),
        city1_code=city1_code,
        city2_code=city2_code,
        crime_code=crime_code
    )

if __name__ == '__main__':
    app.run(debug=False)
