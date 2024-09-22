from app.db import db


# product_urls = [
#     "https://www.amazon.es/Esencia-natural-chocolate-Az%C3%BAcares-a%C3%B1adidos/dp/B07HB5G9RX?pd_rd_w=jhaVJ&content-id=amzn1.sym.facf7f17-8601-4d92-88f5-b69918861ce5&pf_rd_p=facf7f17-8601-4d92-88f5-b69918861ce5&pf_rd_r=RVT69FK8089TW5FX8AW1&pd_rd_wg=T9D7j&pd_rd_r=851f3b9b-0e7b-4c4b-be6e-3492bf329774&pd_rd_i=B07HB5G9RX&ref_=pd_bap_d_grid_rp_0_1_ec_pr_pd_hp_d_atf_rp_4_i&th=1",
#     "https://www.amazon.es/ASUS-Vivobook-Go-E1504GA-NJ486W-Ordenador/dp/B0CSKCNKT5/?_encoding=UTF8&pd_rd_w=UobfP&content-id=amzn1.sym.c88e548c-4fec-4b31-ae8d-af58552edecb&pf_rd_p=c88e548c-4fec-4b31-ae8d-af58552edecb&pf_rd_r=YANGMMB4WZYZZ0FJWYYA&pd_rd_wg=iUE1B&pd_rd_r=50530db5-245e-43ff-adf2-62aa74ff58b9&ref_=pd_hp_d_atf_unk",
#     "https://www.amazon.es/Cuarteto-Oxford-Elizabeth-revolucionaron-Filosof%C3%ADa-ebook/dp/B0CL5JQWL3/?_encoding=UTF8&pd_rd_w=5SmWi&content-id=amzn1.sym.a6b39527-9540-4776-89bb-7d156154a921&pf_rd_p=a6b39527-9540-4776-89bb-7d156154a921&pf_rd_r=Z1S8MB9F93HAJAB185JJ&pd_rd_wg=E5las&pd_rd_r=1244f73b-7b89-4bfe-bb9a-49a58b2529f2&ref_=pd_hp_d_btf_cr_cartx",
# ]


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2))
    price_trigger = db.Column(db.Float(precision=2), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    create_datetime = db.Column(db.DateTime, nullable=False)

    def __init__(
        self, name: str, price: float, trigger: float, url: str, created: str
    ) -> None:
        self.name = name
        self.price = price
        self.price_trigger = trigger
        self.url = url
        self.create_datetime = created

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "price_trigger": self.price_trigger,
            "create_datetime": self.create_datetime.isoformat(),
        }

    @classmethod
    def find_by_name(cls, name: str) -> "ProductModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls: "ProductModel") -> list:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_all_from_db(cls: "ProductModel") -> None:
        db.session.query(cls).delete()
        db.session.commit()
