from flask import Blueprint, request, jsonify
from models import RephraseRequest, db
from utils import simple_paraphrases
import json

rephrase_bp = Blueprint('rephrase_bp', __name__)

@rephrase_bp.route('/', methods=['POST'])
def rephrase():
    """
    POST JSON: { "sentence": "Your sentence here." }
    Response: { "original": "...", "variants": [...] }
    """
    data = request.get_json(force=True, silent=True)
    if not data or 'sentence' not in data:
        return jsonify({"error": "Please provide JSON body with 'sentence' field."}), 400

    sentence = data['sentence'].strip()
    if not sentence:
        return jsonify({"error": "Sentence cannot be empty."}), 400

    variants = simple_paraphrases(sentence, max_variants=5)

    # Log to DB
    rr = RephraseRequest(original_text=sentence, outputs=json.dumps(variants))
    db.session.add(rr)
    db.session.commit()

    return jsonify({
        "original": sentence,
        "variants": variants
    })
