from database import db
from sqlalchemy import select

G = 6.6743 * 10 ** (-11)

class Body(db.Model):
    __tablename__ = "celestial_bodies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    body_type = db.Column(db.Integer, nullable=False) # 0 - star, 1 - planet, 2 - moon
    orbit_radius = db.Column(db.Float)
    parent_id = db.Column(db.Integer, db.ForeignKey("celestial_bodies.id"))

    parent = db.relationship("Body", remote_side=[id], back_populates="children")
    children = db.relationship("Body", back_populates="parent")

    def get_orbital_velocity(self, radius):
        return (G*self.mass / radius)**0.5

    def get_own_orbital_velocity(self):
        return self.parent.get_orbital_velocity(self.orbit_radius)

def calculate_rvel_with_escape(body, target_v, orbit_radius):
    v_inf = abs(target_v - body.get_own_orbital_velocity())
    mu = G*body.mass
    return (v_inf**2 + (2*mu/orbit_radius))**0.5

def calculate_velocity(source, source_radius, dest, dest_radius):
    if source is dest:
        mu = G*source.mass
        a = (source_radius + dest_radius) / 2
        v1 = (mu*(2/source_radius - 1/a))**0.5
        v2 = (mu*(2/dest_radius - 1/a))**0.5
        return v1, v2

    if source.body_type > dest.body_type:
        target_v1, target_v2 = calculate_velocity(source.parent, source.orbit_radius, dest, dest_radius)
        return calculate_rvel_with_escape(source, target_v1, source_radius), target_v2
    elif source.body_type < dest.body_type:
        target_v1, target_v2 = calculate_velocity(source, source_radius, dest.parent, dest.orbit_radius)
        return target_v1, calculate_rvel_with_escape(dest, target_v2, dest_radius)
    else:
        target_v1, target_v2 = calculate_velocity(source.parent, source.orbit_radius, dest.parent, dest.orbit_radius)
        return calculate_rvel_with_escape(source, target_v1, source_radius), calculate_rvel_with_escape(dest, target_v2, dest_radius)

def calculate_dv(source, source_height, dest, dest_height, include_capture_burn):
    v1, v2 = calculate_velocity(source, source_height+source.radius, dest, dest_height+dest.radius)
    dv1 = abs(v1 - source.get_orbital_velocity(source_height+source.radius))
    dv2 = abs(v2 - dest.get_orbital_velocity(dest_height+dest.radius))
    return dv1 + include_capture_burn*dv2

def get_planet(name):
    something = select(Body).where(Body.name == name)
    result = db.session.execute(something).scalars().all()
    if len(result) < 1:
        return None
    return result[0]

def hardcode_planets():
    if get_planet("Kerbin") is not None:
        return

    Kerbol = Body(name="Kerbol", mass=1.7565459E28, radius=261600000, body_type=0)

    db.session.add(Kerbol)
    db.session.commit()

    Moho = Body(name="Moho", mass=2.5263314E21, radius=250000, body_type=1, orbit_radius=5263138304, parent=Kerbol)
    Eve = Body(name="Eve", mass=1.2243980E23, radius=700000, body_type=1, orbit_radius=9832684544, parent=Kerbol)
    Kerbin = Body(name="Kerbin", mass=5.2915158E22, radius=600000, body_type=1, orbit_radius=13599840256, parent=Kerbol)
    Duna = Body(name="Duna", mass=4.5154270E21, radius=320000, body_type=1, orbit_radius=20726155264, parent=Kerbol)
    Dres = Body(name="Dres", mass=3.2190937E20, radius=138000, body_type=1, orbit_radius=40839348203, parent=Kerbol)
    Jool = Body(name="Jool", mass=4.2332127E24, radius=6000000, body_type=1, orbit_radius=68773560320, parent=Kerbol)
    Eeloo = Body(name="Eeloo", mass=1.1149224E21, radius=210000, body_type=1, orbit_radius=90118820000, parent=Kerbol)

    db.session.add_all([Moho, Eve, Kerbin, Duna, Dres, Jool, Eeloo])
    db.session.commit()

    Gilly = Body(name="Gilly", mass=1.2420363E17, radius=13000, body_type=2, orbit_radius=31500000, parent=Eve)
    Mun = Body(name="Mun", mass=9.7599066E20, radius=200000, body_type=2, orbit_radius=12000000, parent=Kerbin)
    Minmus = Body(name="Minmus", mass=2.6457580E19, radius=60000, body_type=2, orbit_radius=47000000, parent=Kerbin)
    Ike = Body(name="Ike", mass=2.7821615E20, radius=130000, body_type=2, orbit_radius=3200000, parent=Duna)
    Laythe = Body(name="Laythe", mass=2.9397311E22, radius=500000, body_type=2, orbit_radius=27184000, parent=Jool)
    Vall = Body(name="Vall", mass=3.1087655E21, radius=300000, body_type=2, orbit_radius=43152000, parent=Jool)
    Tylo = Body(name="Tylo", mass=4.2332127E22, radius=600000, body_type=2, orbit_radius=68500000, parent=Jool)
    Bop = Body(name="Bop", mass=3.7261090E19, radius=65000, body_type=2, orbit_radius=128500000, parent=Jool)
    Pol = Body(name="Pol", mass=1.0813507E19, radius=44000, body_type=2, orbit_radius=179890000, parent=Jool)

    db.session.add_all([Gilly, Mun, Minmus, Ike, Dres, Laythe, Vall, Tylo, Bop, Pol])
    db.session.commit()

def wrong_input(request_data):
    for point in request_data:
        if not ("location" in point.keys() and "alt" in point.keys()):
            return True
        try:
            if int(point["alt"]) <= 0:
                return True
        except (ValueError, TypeError):
            return True
    return False

def get_response(request_data):
    if wrong_input(request_data):
        return {"dv": "Error: invalid input"}
    dv = 0
    prev = request_data[0]
    for stop in request_data[1:]:
        source = get_planet(prev["location"])
        dest = get_planet(stop["location"])
        if source is None or dest is None:
            return {"dv": "Error: invalid input"}
        dv += calculate_dv(source, int(prev["alt"]), dest, int(stop["alt"]), 1)
        prev = stop
    dv = round(dv, 1)
    return {"dv": dv}
