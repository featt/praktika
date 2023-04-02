from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1289@localhost:5432/mathematical_vertical'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

class ParticipationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)

class Responsible(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    location = db.Column(db.String(255))

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(255), nullable=False)
    number_of_teachers = db.Column(db.Integer)

class TeacherTraining(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255))
    hours = db.Column(db.Integer)
    specialization = db.Column(db.String(255))
    number_of_teachers = db.Column(db.Integer)

app = create_app()

# ParticipationStatus CRUD
@app.route('/participationStatus', methods=['GET'])
def get_participationstatus():
    participationstatus = ParticipationStatus.query.all()
    return jsonify([p.status for p in participationstatus])


@app.route('/participationStatus', methods=['POST'])
def create_participationstatus():
    status = request.json['status']
    participationstatus = ParticipationStatus(status=status)
    db.session.add(participationstatus)
    db.session.commit()
    return jsonify({'message': 'ParticipationStatus created'}), 201


@app.route('/participationStatus/<int:id>', methods=['PUT'])
def update_participationstatus(id):
    participationstatus = ParticipationStatus.query.get_or_404(id)
    participationstatus.status = request.json['status']
    db.session.commit()
    return jsonify({'message': 'ParticipationStatus updated'})


@app.route('/participationStatus/<int:id>', methods=['DELETE'])
def delete_participationstatus(id):
    participationstatus = ParticipationStatus.query.get_or_404(id)
    db.session.delete(participationstatus)
    db.session.commit()
    return jsonify({'message': 'ParticipationStatus deleted'})


# Responsible CRUD
@app.route('/responsible', methods=['GET'])
def get_responsible():
    responsible = Responsible.query.all()
    return jsonify([str(r) for r in responsible])


@app.route('/responsible', methods=['POST'])
def create_responsible():
    name = request.json['name']
    position = request.json['position']
    phone = request.json['phone']
    email = request.json['email']
    responsible = Responsible(name=name, position=position, phone=phone, email=email)
    db.session.add(responsible)
    db.session.commit()
    return jsonify({'message': 'Responsible created'}), 201


@app.route('/responsible/<int:id>', methods=['PUT'])
def update_responsible(id):
    responsible = Responsible.query.get_or_404(id)
    responsible.name = request.json['name']
    responsible.position = request.json['position']
    responsible.phone = request.json['phone']
    responsible.email = request.json['email']
    db.session.commit()
    return jsonify({'message': 'Responsible updated'})


@app.route('/responsible/<int:id>', methods=['DELETE'])
def delete_responsible(id):
    responsible = Responsible.query.get_or_404(id)
    db.session.delete(responsible)
    db.session.commit()
    return jsonify({'message': 'Responsible deleted'})

@app.route('/equipment', methods=['POST'])
def create_equipment():
    name = request.json.get('name')
    address = request.json.get('address')
    location = request.json.get('location')
    equipment = Equipment(name=name, address=address, location=location)
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'id': equipment.id}), 201


@app.route('/equipment', methods=['GET'])
def get_all_equipment():
    equipment = Equipment.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'address': e.address, 'location': e.location} for e in equipment]), 200


@app.route('/equipment/<int:id>', methods=['GET'])
def get_equipment(id):
    equipment = Equipment.query.filter_by(id=id).first()
    if not equipment:
        return jsonify({'error': 'Equipment item not found'}), 404
    return jsonify({'id': equipment.id, 'name': equipment.name, 'address': equipment.address, 'location': equipment.location}), 200

@app.route('/equipment/<int:id>', methods=['PUT'])
def update_equipment(id):
    equipment = Equipment.query.filter_by(id=id).first()
    if not equipment:
        return jsonify({'error': 'Equipment item not found'}), 404
    name = request.json.get('name')
    address = request.json.get('address')
    location = request.json.get('location')
    if name:
        equipment.name = name
    if address:
        equipment.address = address
    if location:
        equipment.location = location
    db.session.commit()
    return jsonify({'id': equipment.id}), 200


@app.route('/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    equipment = Equipment.query.filter_by(id=id).first()
    if not equipment:
        return jsonify({'error': 'Equipment item not found'}), 404
    db.session.delete(equipment)
    db.session.commit()
    return '', 204

# Teacher CRUD
@app.route('/teachers', methods=['POST'])
def create_teacher():
    specialization = request.json['specialization']
    number_of_teachers = request.json['number_of_teachers']
    teacher = Teachers(specialization=specialization, number_of_teachers=number_of_teachers)
    db.session.add(teacher)
    db.session.commit()
    return jsonify({'id': teacher.id, 'specialization': teacher.specialization, 'number_of_teachers': teacher.number_of_teachers}), 201

@app.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teachers.query.all()
    return jsonify([{'id': teacher.id, 'specialization': teacher.specialization, 'number_of_teachers': teacher.number_of_teachers} for teacher in teachers]), 200

@app.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    teacher = Teachers.query.get_or_404(teacher_id)
    return jsonify({'id': teacher.id, 'specialization': teacher.specialization, 'number_of_teachers': teacher.number_of_teachers}), 200

@app.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    teacher = Teachers.query.get_or_404(teacher_id)
    teacher.specialization = request.json['specialization']
    teacher.number_of_teachers = request.json['number_of_teachers']
    db.session.commit()
    return jsonify({'id': teacher.id, 'specialization': teacher.specialization, 'number_of_teachers': teacher.number_of_teachers}), 200

@app.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    teacher = Teachers.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return '', 204


# teacher training CRUD
@app.route('/teacher_training', methods=['POST'])
def create_teacher_training():
    request_data = request.get_json()
    new_teacher_training = TeacherTraining(course_name=request_data['course_name'],
                                           organization=request_data.get('organization'),
                                           hours=request_data.get('hours'),
                                           specialization=request_data.get('specialization'),
                                           number_of_teachers=request_data.get('number_of_teachers'))
    db.session.add(new_teacher_training)
    db.session.commit()
    return jsonify(new_teacher_training.id)


@app.route('/teacher_training/<int:teacher_training_id>', methods=['GET'])
def get_teacher_training(teacher_training_id):
    teacher_training = TeacherTraining.query.filter_by(id=teacher_training_id).first()
    if teacher_training is None:
        return jsonify('TeacherTraining not found'), 404
    return jsonify({'id': teacher_training.id,
                    'course_name': teacher_training.course_name,
                    'organization': teacher_training.organization,
                    'hours': teacher_training.hours,
                    'specialization': teacher_training.specialization,
                    'number_of_teachers': teacher_training.number_of_teachers})


@app.route('/teacher_training/<int:teacher_training_id>', methods=['PUT'])
def update_teacher_training(teacher_training_id):
    teacher_training = TeacherTraining.query.filter_by(id=teacher_training_id).first()
    if teacher_training is None:
        return jsonify('TeacherTraining not found'), 404
    request_data = request.get_json()
    teacher_training.course_name = request_data.get('course_name', teacher_training.course_name)
    teacher_training.organization = request_data.get('organization', teacher_training.organization)
    teacher_training.hours = request_data.get('hours', teacher_training.hours)
    teacher_training.specialization = request_data.get('specialization', teacher_training.specialization)
    teacher_training.number_of_teachers = request_data.get('number_of_teachers', teacher_training.number_of_teachers)
    db.session.commit()
    return jsonify('TeacherTraining updated')

@app.route('/teacher_training/<int:teacher_training_id>', methods=['DELETE'])
def delete_teacher_training(teacher_training_id):
    teacher_training = TeacherTraining.query.filter_by(id=teacher_training_id).first()
    if teacher_training is None:
        return jsonify('TeacherTraining not found'), 404
    db.session.delete(teacher_training)
    db.session.commit()
    return jsonify('TeacherTraining deleted')


if __name__ == '__main__':
    app.run(debug=True)