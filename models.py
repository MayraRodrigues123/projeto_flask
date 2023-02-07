from biblioteca import db

class Fotos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome