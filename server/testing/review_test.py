from app import app, db
from server.models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns
            
            # Create Customer and Item instances to associate with the Review
            c = Customer(name="John Doe")
            i = Item(name="Product A", price=19.99)
            
            # Add Customer and Item to the session
            db.session.add_all([c, i])
            db.session.commit()

            # Now create the Review instance, passing the Customer and Item
            r = Review(comment='great!', customer=c, item=i)
            
            # Add the review to the session and commit it
            db.session.add(r)
            db.session.commit()
            
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create Customer and Item instances
            c = Customer(name="Jane Doe")
            i = Item(name="Product B", price=29.99)
            
            # Add Customer and Item to the session
            db.session.add_all([c, i])
            db.session.commit()

            # Create Review instance, passing the Customer and Item
            r = Review(comment='great!', customer=c, item=i)
            
            # Add the review to the session and commit it
            db.session.add(r)
            db.session.commit()

            # check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id
            # check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
