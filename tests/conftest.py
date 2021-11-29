from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
import pytest
from app.oauth2 import create_access_token
import json
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try: 
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data={"username":"thiere","email":"thiern@gmail.com","password":"thierno"}
    res=client.post('/api/v1/users/',json=user_data)
    assert res.status_code == 201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user
    
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
        }
    return client
    


    # def create_product_model(product):
    #     return models.I(**product)
    # product_map=map(create_product_model,invoice)
    # prods=list(product_map)
    # for x in prods:
    #     print(x)
    # session.add_all(prods)
    # session.commit()
    # inv=json.dumps(invoice)
    # for inb  in invoice:
    #     print(inb)
        # new_invoice = models.Invoice(invoice_owner_id=test_user['id'],payment_due=(inv['value_net']-inv['actual_payment']), **inv)
        # session.add(new_invoice)
        # session.commit()
        # session.refresh(new_invoice)
    
        # new_id=new_invoice.id
        # for invoice_item in inv['items']:
        #     prod=invoice_item['product_name']
        #     quant=invoice_item['quantity']
        #     #verify if this product exist
        #     p= session.query(models.Product).filter(models.Product.product_name==prod).first()
        #     p.quantity_left-=quant
        #     session.commit()
        #     new_invoice_item = models.InvoiceItem(invoice_id=new_id,**invoice_item.dict())
        #     session.add(new_invoice_item)
        #     session.commit()
    
    