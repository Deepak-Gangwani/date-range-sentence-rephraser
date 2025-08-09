from flask import Blueprint, request, jsonify
from models import DateRequest, db
from utils import generate_date_list
import json

date_bp = Blueprint('date_bp', __name__)

SUPPORTED = ['till_yesterday', 'till_tomorrow', 'next_month', 'last_7_days', 'this_week']

@date_bp.route('/generate', methods=['GET'])
def generate():
    range_key = request.args.get('range')
    if not range_key:
        return jsonify({"error": "Missing 'range' query parameter. Supported values: " + ", ".join(SUPPORTED)}), 400

    if range_key not in SUPPORTED:
        return jsonify({"error": f"Unsupported range '{range_key}'. Supported: {', '.join(SUPPORTED)}"}), 400

    try:
        dates = generate_date_list(range_key)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Log to DB
    dr = DateRequest(range_key=range_key, generated_dates=json.dumps(dates))
    db.session.add(dr)
    db.session.commit()

    return jsonify({
        "range": range_key,
        "count": len(dates),
        "dates": dates
    })
